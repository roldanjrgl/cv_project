import os
os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'
import time

from mlhub_collect_data import *
from mlhub_helper import *
from data_preprocessing import *
from plot_images import *

def main():
    download = True
    convert = False
    plot = False
    print_collection_info = False
    # choose number of items you want to download
    max_items = 5
    data_all_labels_path = './data_all_labels/ref_landcovernet_v1_labels'
    collection_id = 'ref_landcovernet_v1_labels'

    if print_collection_properties:
        print_collection_properties(collection_id=collection_id)
        print_land_cover_labels(collection_id)
        

    if download:
        start = time.time()
        # items = get_items(collection_id,cloud_and_shadow=True, max_items=max_items)
        items = get_items(collection_id, max_items=max_items)
        download_rgb_labels_and_source(items)
        end = time.time()
        print(f'Time downloading = {end - start}')

    if convert:
        # convert_source_to_png()
        # convert_label_to_png()
        convert_all_labels_to_png(data_all_labels_path)

    if plot:
        label_path = 'data/ref_landcovernet_v1_labels_38PKT_29/labels/38PKT_29_2018_LC_10m.tif'
        plot_label(label_path=label_path)


if __name__ == "__main__":
    main()