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
from data_preprocessing import *
from plot_images import *

def main():
    download = True
    convert = False
    plot = False


    collection_id = 'ref_landcovernet_v1_labels'
    # print_collection_properties(collection_id=collection_id)
    # print_land_cover_labels(collection_id)

    max_items = 1
    items = get_items(collection_id,cloud_and_shadow=True, max_items=max_items)

    if download:
        download_rgb_labels_and_source(items)

    if convert:
        convert_source_to_png()
        convert_label()

    if plot:
        label_path = 'data/ref_landcovernet_v1_labels_38PKT_29/labels/38PKT_29_2018_LC_10m.tif'
        plot_label(label_path=label_path)


if __name__ == "__main__":
    main()