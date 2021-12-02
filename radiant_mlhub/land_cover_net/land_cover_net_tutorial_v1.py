import os
os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'

import urllib.parse
import re
from pathlib import Path
import itertools as it
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from tqdm.notebook import tqdm
from radiant_mlhub import client, get_session


# ==============================================
# Listing Collection Properties
# ==============================================
collection_id = 'ref_landcovernet_v1_labels'
collection = client.get_collection(collection_id)

print(f'Description: {collection["description"]}')
print(f'License: {collection["license"]}')
print(f'DOI: {collection["sci:doi"]}')
print(f'Citation: {collection["sci:citation"]}')

# ==============================================
# Finding Possible Land Cover Labels
# ==============================================
items = client.list_collection_items(collection_id, limit=1)

first_item = next(items)

label_classes = first_item['properties']['label:classes']
for label_class in label_classes:
    print(f'Classes for {label_class["name"]}')
    for c in sorted(label_class['classes']):
        print(f'- {c}')

# ==============================================
# Downloading Assets
# ==============================================
items_pattern = re.compile(r'^/mlhub/v1/collections/(\w+)/items/(\w+)$')


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
    

def download_labels_and_source(item, assets=None, output_dir='./data'):
    """Downloads all label and source imagery assets associated with a label item that match the given asset types.
    """
    
    # Follow all source links and add all assets from those
    def _get_download_args(link):
        # Get the item ID (last part of the link path)
        source_item_path = urllib.parse.urlsplit(link['href']).path
        source_item_collection, source_item_id = items_pattern.fullmatch(source_item_path).groups()
        source_item = client.get_collection_item(source_item_collection, source_item_id)

        source_download_dir = download_dir / 'source'
        source_download_dir.mkdir(exist_ok=True)
        
        matching_source_assets = [
            asset 
            for asset in source_item.get('assets', {}) 
            if assets is None or asset in assets
        ] 
        return [
            (source_item, asset, source_download_dir) 
            for asset in matching_source_assets
        ]

    
    download_args = []
    
    download_dir = Path(output_dir) / item['id']
    download_dir.mkdir(parents=True, exist_ok=True)
    
    labels_download_dir = download_dir / 'labels'
    labels_download_dir.mkdir(exist_ok=True)

    # Download the labels assets
    matching_assets = [
        asset 
        for asset in item.get('assets', {}) 
        if assets is None or asset in assets
    ]

    for asset in matching_assets:
        download_args.append((item, asset, labels_download_dir))
        
    source_links = [link for link in item['links'] if link['rel'] == 'source']
    
    with ThreadPoolExecutor(max_workers=16) as executor:
        for argument_batch in executor.map(_get_download_args, source_links):
            download_args += argument_batch
        
    print(f'Downloading {len(download_args)} assets...')
    with ThreadPoolExecutor(max_workers=16) as executor:
        with tqdm(total=len(download_args)) as pbar:
            for _ in executor.map(lambda triplet: download(*triplet), download_args):
                pbar.update(1)
    

# ==============================================
# Download Assets for 1 Item
# ==============================================
items = get_items(
    collection_id,
    max_items=1
)

for item in items:
    download_labels_and_source(item, assets=['labels', 'B02', 'B03', 'B04'])

# ==============================================
# Filtering on Land Cover Type
# ==============================================
items = get_items(
    collection_id,
    classes=['Woody Vegetation'],
    max_items=1,
)

for item in items:
    download_labels_and_source(item, assets=['labels', 'B02', 'B03', 'B04'])

# ==============================================
# Download All Assets
# ==============================================
client.download_archive(collection_id, output_dir='./data')