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