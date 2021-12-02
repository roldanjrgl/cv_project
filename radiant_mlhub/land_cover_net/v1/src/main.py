import os
os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'
# import urllib.parse
# import re
# from pathlib import Path
# import itertools as it
# from functools import partial
# from concurrent.futures import ThreadPoolExecutor
# from tqdm.notebook import tqdm
# from radiant_mlhub import client, get_session

from mlhub_collect_data import *
from mlhub_helper import *

def main():
    collection_id = 'ref_landcovernet_v1_labels'
    print_collection_properties(collection_id=collection_id)
    print_land_cover_labels(collection_id)

    max_items = 5
    items = get_items(collection_id, max_items=max_items)
    download_rgb_labels_and_source(items)


if __name__ == "__main__":
    main()