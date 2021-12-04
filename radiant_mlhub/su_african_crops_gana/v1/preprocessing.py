import os
import matplotlib.pyplot as plt
import rasterio as rio
import numpy as np
from fastai.vision.all import *


def convert_label_to_png(image_chip_label_path, image_chip_label_name, image_chip_name, data_png_path):
    label = rio.open(image_chip_label_path)
    band1 = label.read(1) 

    save_to_path = data_png_path + '/' + image_chip_name
    if os.path.isdir(save_to_path) == False:
        os.mkdir(save_to_path)

    save_to_path = save_to_path + '/labels/'
    if os.path.isdir(save_to_path) == False:
        os.mkdir(save_to_path)

    plt.imsave(save_to_path + 'labels' + '.png', band1.astype('uint8'))


def convert_all_labels_to_png(all_labels_path):
    # if folder for data_png doesn't exist, create one
    data_png_path = '../data_png'

    if os.path.isdir(data_png_path) == False:
        os.mkdir(data_png_path)

    for image_chip_path in Path(all_labels_path).ls():
        image_chip_label_name = str(image_chip_path)[-36:]
        print(image_chip_label_name)
        image_chip_name = image_chip_label_name[:-14] + image_chip_label_name[-7:]
        print(image_chip_name)
        print(image_chip_name + '/labels.tif')

        image_chip_label_path = all_labels_path + '/' + image_chip_label_name + '/labels.tif'
        convert_label_to_png(image_chip_label_path, image_chip_label_name, image_chip_name, data_png_path)


def convert_source_to_png(data_source_path, name):
    source = rio.open(data_source_path)
    red = source.read(4)
    green = source.read(3)
    blue = source.read(2)

    rgb = np.dstack((red, green, blue))
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    # plt.imsave(source_day_dir + '/' +  source_day + '.png', rgb.astype('uint8'))
    plt.imsave(name + '.png', rgb.astype('uint8'))


def convert_all_sources_to_png(all_sources_path):
    data_png_path = '../data_png'

    if os.path.isdir(data_png_path) == False:
        os.mkdir(data_png_path)
    
    for image_chip_path in Path(all_sources_path).ls():
        print(image_chip_path)
        image_chip_source_name = str(image_chip_path)[-50:]
        print(image_chip_source_name)

        image_chip_name = image_chip_source_name[:-11]
        print(image_chip_name)
        image_chip_name = image_chip_name[:-17] + image_chip_name[-7:]
        print(image_chip_name)
