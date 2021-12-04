import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np

def convert_source_to_png(data_source_path, name):
    source = rio.open(data_source_path)
    red = source.read(4)
    green = source.read(3)
    blue = source.read(2)
    # red = source.read(5)
    # green = source.read(6)
    # blue = source.read(7)

    rgb = np.dstack((red, green, blue))
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    # plt.imsave(source_day_dir + '/' +  source_day + '.png', rgb.astype('uint8'))
    plt.imsave(name + '.png', rgb.astype('uint8'))
