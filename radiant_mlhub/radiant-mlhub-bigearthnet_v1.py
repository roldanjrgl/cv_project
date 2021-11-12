import os
import urllib.parse
import re
from pathlib import Path
import itertools as it
from functools import partial
from radiant_mlhub import client, get_session


# ======================================================
# Authentication
# ======================================================
os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'

# ======================================================
# List BigEarthNet Collections
# ======================================================
def ben_filter(collection):
    # NOTE: The "or" statements below ensure that if the value of collection['title'] or collection['description']
    #  are None we can still use the .lower() function without raising an exception.
    return 'bigearthnet' in collection['id'].lower() \
        or 'bigearthnet' in (collection.get('title') or '').lower() \
        or 'bigearthnet' in (collection.get('description') or '').lower()

# Get list of all collections
all_collections = client.list_collections()

# Filter to only the BigEarthNet collections and print some key information
for collection in filter(ben_filter, all_collections):
    collection_id = collection['id']
    license = collection.get('license', 'N/A')
    citation = collection.get('sci:citation', 'N/A')
    stac_extensions = collection.get('stac_extensions') or []

    print(f'ID:       {collection_id}\nLicense:  {license}\nCitation: {citation}\nSTAC Extensions: {stac_extensions}\n')


# ======================================================
# Download Source Imagery & Labels
# ======================================================

def filter_item(item, classes=None, cloud_and_shadow=None, seasonal_snow=None):
    """Function to be used as an argument to Python's built-in filter function that filters out any items that 
    do not match the given classes, cloud_and_shadow, and/or seasonal_snow values.
    
    If any of these filter arguments are set to None, they will be ignored. For instance, using 
    filter_item(item, cloud_and_shadow=True) will only return items where item['properties']['cloud_and_shadow'] == 'true', 
    and will not filter based on classes/labels, or seasonal_snow.
    """
    # Match classes, if provided
    
    item_labels = item['properties'].get('labels', [])
    if classes is not None and not any(label in classes for label in item_labels):
        return False
    
    # Match cloud_and_shadow, if provided
    item_cloud_and_shadow = item['properties'].get('cloud_and_shadow', 'false') == 'true'
    if cloud_and_shadow is not None and item_cloud_and_shadow != cloud_and_shadow:
        return False
    
    # Match seasonal_snow, if provided
    item_seasonal_snow = item['properties'].get('seasonal_snow', 'false') == 'true'
    if seasonal_snow is not None and item_seasonal_snow != seasonal_snow:
        return False
    
    return True


def get_items(collection_id, classes=None, cloud_and_shadow=None, seasonal_snow=None, max_items=1):
    """Generator that yields up to max_items items that match the given classes, cloud_and_shadow, and seasonal_snow 
    values. Setting one of these filter arguments to None will cause that filter to be ignored (e.g. classes=None 
    means that items will not be filtered by class/label).
    """
    filter_fn = partial(
        filter_item, 
        classes=classes, 
        cloud_and_shadow=cloud_and_shadow, 
        seasonal_snow=seasonal_snow
    )
    filtered = filter(
        filter_fn, 

        # Note that we set the limit to None here because we want to limit based on our own filters. It is not 
        #  recommended to use limit=None for the client.list_collection_items method without implementing your 
        #  own limits because the bigearthnet_v1_labels collection contains hundreds of thousands of items and 
        #  looping over these items without limit may take a very long time.
        client.list_collection_items(collection_id, limit=None)
    )
    yield from it.islice(filtered, max_items)
    

def download(item, asset_key, output_dir='./data'):
    """Downloads the given item asset by looking up that asset and then following the "href" URL."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Try to get the given asset and return None if it does not exist
    asset = item.get('assets', {}).get(asset_key)
    if asset is None:
        print(f'Asset "{asset_key}" does not exist in this item')
        return None
    
    # Try to get the download URL from the asset and return None if it does not exist
    download_url = asset.get('href')
    if download_url is None:
        print(f'Asset {asset_key} does not have an "href" property, cannot download.')
        return None
    
    session = get_session()
    r = session.get(download_url, allow_redirects=True, stream=True)
    
    filename = urllib.parse.urlsplit(r.url).path.split('/')[-1]
    output_path = Path(output_dir) / filename

    
    with output_path.open('wb') as dst:
        for chunk in r.iter_content(chunk_size=512 * 1024):
            if chunk:
                dst.write(chunk)
    
    print(f'Downloaded to {output_path.resolve()}')


# ======================================================
# Select an Item
# ======================================================

collection_id = 'bigearthnet_v1_labels'

items = get_items(
    collection_id,
    # classes=['Coniferous forest', 'Rice fields'],
    cloud_and_shadow=False,
    seasonal_snow=False,
    max_items=10
)
first_item = next(items)

print (f'ID: {first_item["id"]}\n')

# Summarize the assets
print('Assets\n------')
for asset_key, asset in first_item['assets'].items():
    print(f'Key: {asset_key}\nTitle: {asset["title"]}\n')

# ======================================================
# Download labels
# ======================================================
download(first_item, 'labels')



# ======================================================
# Download labels
# ======================================================
items_pattern = re.compile(r'^/mlhub/v1/collections/(\w+)/items/(\w+)$')

# ======================================================
# Download Source Imagery
# ======================================================

# Summarize the source links
print('Sources\n------------')
for link in first_item['links']:
    if link['rel'] == 'source':
        # Get the item ID (last part of the link path)
        item_path = urllib.parse.urlsplit(link['href']).path
        item_collection, item_id = items_pattern.fullmatch(item_path).groups()
        item = client.get_collection_item(item_collection, item_id)
        
        item_id = item["id"]
        platform = item["properties"].get('platform', 'N/A')
        n_assets = len(item['assets'])
        print(f'ID: {item_id}\nPlatform: {platform}\nNumber of Assets: {n_assets}\n')
        
        # Only summarize the first 4 bands...
        for asset_key, asset in it.islice(item['assets'].items(), 4):
            media_type = asset['type']
            band_names = [band['common_name'] for band in asset['eo:bands']]
            print(f'Key: {asset_key}\nAsset Type: {media_type}\nBands: {band_names}\n')
            
        print('...')

source_item = client.get_collection_item('bigearthnet_v1_source', 'bigearthnet_v1_source_S2B_MSIL2A_20170709T094029_30_50')

rgb_bands = ['B02', 'B03', 'B04']

for asset_key in rgb_bands:
    download(source_item, asset_key)

# ======================================================
# Download All Assets
# ======================================================
output_dir = Path('./data')

print(f'Downloading {collection_id} archive...')
# client.download_archive(collection_id, output_dir=output_dir)
