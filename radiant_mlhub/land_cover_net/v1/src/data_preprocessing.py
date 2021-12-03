import numpy
from fastai.vision.all import *
import rasterio as rio

def get_source_rgb(path_dict):
    # reference_got_from:  https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    red = rio.open(path_dict['red']).read(1) # B4
    green = rio.open(path_dict['green']).read(1) # B3
    blue = rio.open(path_dict['blue']).read(1) # B2

    rgb = np.dstack((red, green, blue))

    # normalize and convert to range 0-255
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    return rgb

def convert_source_to_png():
    # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    rgbnl = {}
    # for loc in Path('data/ref_landcovernet_v1_labels_38PKT_25/source').ls(): 
    for img in Path('data/ref_landcovernet_v1_labels_38PKT_29/source').ls(): 
        print(img)
        if re.search('.*0101_B04_10m.tif', str(img)) : rgbnl['red'] = img 
        if re.search('.*0101_B03_10m.tif', str(img)) : rgbnl['green'] = img
        if re.search('.*0101_B02_10m.tif', str(img)) : rgbnl['blue'] = img
        if re.search('.*0101_B08_10m.tif', str(img)) : rgbnl['nir'] = img
    rgb = get_source_rgb(rgbnl)
    filename = 'rbd_testing'
    plt.imsave(filename + '.png', rgb.astype('uint8'))


def get_label(path_dict):
    # reference_got_from:  https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    channel = rio.open(path_dict['band']).read(1)

    # rgb = np.dstack((red, green, blue))

    # normalize and convert to range 0-255
    channel_normalized = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype(int)
    return channel_normalized 


def convert_label():
    # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    rgbnl = {}
    for img in Path('data/ref_landcovernet_v1_labels_38PKT_29/labels').ls(): 
        print(img)
        if re.search('.*LC_10m.tif', str(img)) : rgbnl['band'] = img 
    rgb = get_label(rgbnl)
    filename = 'label_testing'
    plt.imsave(filename + '.png', rgb.astype('uint8'))

