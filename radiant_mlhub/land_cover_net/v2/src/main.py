import os
os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'
import time

from mlhub_collect_data import *
from mlhub_helper import *
from data_preprocessing import *
from plot_images import *

def main():
    all_source_path = 'data_all_source'
    all_labels_path = './data_all_labels/ref_landcovernet_v1_labels'

    convert_all_sources_to_png(all_source_path)
    convert_all_labels_to_png(all_labels_path)
        
if __name__ == "__main__":
    main()