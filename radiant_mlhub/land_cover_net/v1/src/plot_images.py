import xarray as xr
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from PIL import Image
import PIL

import rasterio
from rasterio.plot import show
from matplotlib import pyplot

# def plot_label(label_path):
#     label = xr.open_rasterio(label_path)
#     fig = plt.figure(figsize=(10,10))
#     plt.imshow(label[1, :, :])
#     plt.colorbar()
#     plt.draw()
#     plt.show()
    # plt.imsave('label' + '.png', label[0, :, :].astype('uint8'))


# def plot_label(label_path):
#     # path = 'data/ref_landcovernet_v1_labels_38PKT_25/labels/38PKT_25_2018_LC_10m.tif'
#     # img = Image.open(path)
#     img = Image.open(label_path)
#     img.show()

#     img_arr = np.array(img)
#     print(img_arr)

def plot_label(label_path):
    src = rasterio.open(label_path)
    image = src.read()
    show(image)
    image_norm = (image - image.min()) / (image.max() - image.min())
    show(image_norm)
    print(image_norm)


label_path = 'data/ref_landcovernet_v1_labels_38PKT_28/source/38PKT_28_20180605_B04_10m.tif' 
plot_label(label_path=label_path)