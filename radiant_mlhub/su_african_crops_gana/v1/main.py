import os
from matplotlib.colors import Colormap
import rasterio as rio
from fastai.vision.all import *

from plotting import *
from exploring import *
from preprocessing import *

os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'


def main():
    explore_dataset()
    pass


if __name__ == "__main__":
    main()