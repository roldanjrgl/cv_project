#!/usr/bin/env python
# coding: utf-8

# <img src='https://radiant-assets.s3-us-west-2.amazonaws.com/PrimaryRadiantMLHubLogo.png' alt='Radiant MLHub Logo' width='300'/>
# 
# # How to use the Radiant MLHub API to browse and download the BigEarthNet dataset
# 
# This Jupyter notebook, which you may copy and adapt for any use, shows basic examples of how to use the API to download labels and source imagery for the BigEarthNet dataset. Full documentation for the API is available at [docs.mlhub.earth](docs.mlhub.earth).
# 
# We'll show you how to set up your authorization, see the list of available collections and datasets, and retrieve the items (the data contained within them) from those collections. 
# 
# Each item in our collection is explained in json format compliant with [STAC](https://stacspec.org/) [label extension](https://github.com/radiantearth/stac-spec/tree/master/extensions/label) definition.

# ## Citation Requirements and Contact Information
# 
# The BigEarthNet archive was constructed by the Remote Sensing Image Analysis [(RSiM)](https://www.rsim.tu-berlin.de/menue/remote_sensing_image_analysis_group/) Group and the Database Systems and Information Management [(DIMA)](https://www.dima.tu-berlin.de/menue/database_systems_and_information_management_group/?no_cache=1) Group at the Technische Universität Berlin [(TU Berlin)](https://www.tu-berlin.de/menue/home/parameter/en/). This work is supported by the European Research Council under the ERC Starting Grant BigEarth and by the German Ministry for Education and Research as Berlin Big Data Center [(BBDC)](http://www.bbdc.berlin/home/).
# 
# The BigEarthNet archive *requires* the a citation of the BigEarthNet paper whenever the archive is used. The citation for this paper is listed below along with contact information for inqueries about the archive and a PDF manual detailing the structure of the archive.
# 
# ## Citation
# 
# G. Sumbul, M. Charfuelan, B. Demir, V. Markl, "[BigEarthNet: A Large-Scale Benchmark Archive for Remote Sensing Image Understanding](http://bigearth.net/static/documents/BigEarthNet_IGARSS_2019.pdf)", IEEE International Geoscience and Remote Sensing Symposium, pp. 5901-5904, Yokohama, Japan, 2019.
# 
# 
# 
# ## Contact Information
# 
# * Website: [www.bigearth.net](www.bigearth.net)
# * Email: contact@bigearth.net
# * Manual: [http://bigearth.net/static/documents/BigEarthNetManual.pdf](http://bigearth.net/static/documents/BigEarthNetManual.pdf)

# ## Dependencies
# 
# This notebook utilizes the [`radiant-mlhub` Python client](https://pypi.org/project/radiant-mlhub/) for interacting with the API. If you are running this notebooks using Binder, then this dependency has already been installed. If you are running this notebook locally, you will need to install this yourself.
# 
# See the official [`radiant-mlhub` docs](https://radiant-mlhub.readthedocs.io/) for more documentation of the full functionality of that library.

# ## Authentication
# 
# ### Create an API Key
# 
# Access to the Radiant MLHub API requires an API key. To get your API key, go to [dashboard.mlhub.earth](https://dashboard.mlhub.earth). If you have not used Radiant MLHub before, you will need to sign up and create a new account. Otherwise, sign in. In the **API Keys** tab, you'll be able to create API key(s), which you will need. *Do not share* your API key with others: your usage may be limited and sharing your API key is a security risk.
# 
# ### Configure the Client
# 
# Once you have your API key, you need to configure the `radiant_mlhub` library to use that key. There are a number of ways to configure this (see the [Authentication docs](https://radiant-mlhub.readthedocs.io/en/latest/authentication.html) for details). 
# 
# For these examples, we will set the `MLHUB_API_KEY` environment variable. Run the cell below to save your API key as an environment variable that the client library will recognize.
# 
# *If you are running this notebook locally and have configured a profile as described in the [Authentication docs](https://radiant-mlhub.readthedocs.io/en/latest/authentication.html), then you do not need to execute this cell.*
# 

# In[ ]:


import os

os.environ['MLHUB_API_KEY'] = 'PASTE_YOUR_API_KEY_HERE'


# In[ ]:


import urllib.parse
import re
from pathlib import Path
import itertools as it
from functools import partial

from radiant_mlhub import client, get_session


# ## List BigEarthNet Collections
# 
# A **collection** in the Radiant MLHub API is a [STAC Collection](https://github.com/radiantearth/stac-spec/tree/master/collection-spec) representing a group of resources (represented as [STAC Items](https://github.com/radiantearth/stac-spec/tree/master/item-spec) and their associated assets) covering a given spatial and temporal extent. A Radiant MLHub collection may contain resources representing training labels, source imagery, or (rarely) both.
# 
# The following cell uses the `client.list_collections` function to list all available collections, and then uses Python's built-in [`filter` function](https://docs.python.org/3/library/functions.html#filter) to filter this to only collections containing `bigearthnet` in the ID, title, description.

# In[ ]:


def ben_filter(collection):
    # NOTE: The "or" statements below ensure that if the value of collection['title'] or collection['description']
    #  are None we can still use the .lower() function without raising an exception.
    return 'bigearthnet' in collection['id'].lower()         or 'bigearthnet' in (collection.get('title') or '').lower()         or 'bigearthnet' in (collection.get('description') or '').lower()

# Get list of all collections
all_collections = client.list_collections()

# Filter to only the BigEarthNet collections and print some key information
for collection in filter(ben_filter, all_collections):
    collection_id = collection['id']
    license = collection.get('license', 'N/A')
    citation = collection.get('sci:citation', 'N/A')
    stac_extensions = collection.get('stac_extensions') or []

    print(f'ID:       {collection_id}\nLicense:  {license}\nCitation: {citation}\nSTAC Extensions: {stac_extensions}\n')


# ## Download Source Imagery & Labels
# 
# > **NOTE:** If you are running these notebooks using Binder these resources will be downloaded to the remote file system that the notebooks are running on and **not to your local file system.** If you want to download the files to your machine, you will need to clone the repo and run the notebook locally.
# 
# The labels in BigEarthNet have three properties.
# 1) An array of land cover type classes contained in the tile
# 2) Whether the tile contains cloud and cloud shadows
# 3) Whether the tile has seasonal snow
# 
# We can filter our download based off one or more of the properties.

# ### Create Download Helpers
# 
# The cell below creates 3 helper functions that we will use to select items from a collection and download the associated assets (source imagery or labels).
# 
# * **`get_items`**
# 
#     This is a [Python generator](https://realpython.com/introduction-to-python-generators/) that yields items from the given collection that match the criteria we give it. For instance, the following code will yield up to 10 items from the BigEarthNet labels collection that contain *either the `'Coniferous forest'` or the `'Rice fields'` labels*:
#     ```python
#     get_items('bigearthnet_v1_labels', classes=['Coniferous forest', 'Rice fields'], max_items=10)
#     ```
# 
# * **`download`** 
# 
#     This function takes an item dictionary and an asset key and downloads the given asset. By default, the asset is downloaded to the current working directory, but this can be changed using the `output_dir` argument.
# 
# * **`filter_item`** 
# 
#     This is a helper function used by the `get_items` function to filter items returned by `client.list_collection_items`.
# 

# In[ ]:


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


# ### Select an Item
# 
# As we saw above, the BigEarthNet dataset is split into two collections: one which contains the labels and one which contains the source imagery. Label items link to their respective source imagery items so we will set our collection ID to `bigearthnet_v1_labels`.

# In[ ]:


collection_id = 'bigearthnet_v1_labels'


# In this next cell we will fetch the first item in the collection which contains either the `Coniferous forest` or `Rice fields` classes, does not contain clouds and cloud shadows, and does not contain seasonal snow. We the display the item ID and summarize the assets associated with this item.

# In[ ]:


items = get_items(
    collection_id,
    classes=['Coniferous forest', 'Rice fields'],
    cloud_and_shadow=False,
    seasonal_snow=False,
    max_items=1
)
first_item = next(items)

print (f'ID: {first_item["id"]}\n')

# Summarize the assets
print('Assets\n------')
for asset_key, asset in first_item['assets'].items():
    print(f'Key: {asset_key}\nTitle: {asset["title"]}\n')


# ### Download Labels
# 
# This item has only a single `labels` asset, which we can download using our helper function.

# In[ ]:


download(first_item, 'labels')


# ### Download Source Imagery
# 
# The following cell fetches all of the source links (links to the source imagery STAC Items in the Radiant MLHub API) associated with the `labels` item above and summarizes the assets associated with these source items.

# In[ ]:


items_pattern = re.compile(r'^/mlhub/v1/collections/(\w+)/items/(\w+)$')

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


# We can see that there is a single source item associated with our labels and that it corresponds to a Sentinel 2 scene. This item has 13 assets (all Cloud-Optimized GeoTIFFs) corresponding to the different bands (we have only summarized the first 4 bands above).
# 
# The following cell downloads each of the 3 RGB band images.

# In[ ]:


source_item = client.get_collection_item('bigearthnet_v1_source', 'bigearthnet_v1_source_S2B_MSIL2A_20170709T094029_30_50')

rgb_bands = ['B02', 'B03', 'B04']

for asset_key in rgb_bands:
    download(source_item, asset_key)


# ### Download All Assets
# 
# Looping through all items and downloading the associated assets may be *very* time-consuming for larger datasets like BigEarthNet. Instead, MLHub provides TAR archives of all collections that can be downloaded using the `/archive/{collection_id}` endpoint. 
# 
# The following cell uses the `client.download_archive` function to download the `bigearthnet_v1_labels` archive to the current working directory.

# In[ ]:


output_dir = Path('./data')

print(f'Downloading {collection_id} archive...')
client.download_archive(collection_id, output_dir=output_dir)


# In[ ]:




