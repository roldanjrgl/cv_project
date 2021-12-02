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


def print_collection_properties(collection_id):
    collection_id = 'ref_landcovernet_v1_labels'
    collection = client.get_collection(collection_id)

    print(f'Description: {collection["description"]}')
    print(f'License: {collection["license"]}')
    print(f'DOI: {collection["sci:doi"]}')
    print(f'Citation: {collection["sci:citation"]}')


def print_land_cover_labels(collection_id):
    items = client.list_collection_items(collection_id, limit=1)

    first_item = next(items)

    label_classes = first_item['properties']['label:classes']
    for label_class in label_classes:
        print(f'Classes for {label_class["name"]}')
        for c in sorted(label_class['classes']):
            print(f'- {c}')