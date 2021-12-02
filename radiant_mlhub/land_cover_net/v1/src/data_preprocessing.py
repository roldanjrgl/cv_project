import numpy
from fastai.vision.all import *
import rasterio as rio

def get_rgb(path_dict):
    # reference_got_from:  https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    red = rio.open(path_dict['red']).read(1) # B4
    green = rio.open(path_dict['green']).read(1) # B3
    blue = rio.open(path_dict['blue']).read(1) # B2

    rgb = np.dstack((red, green, blue))

    # normalize and convert to range 0-255
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    return rgb

def convert_images():
    # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    rgbnl = {}
    # for loc in Path('data/ref_landcovernet_v1_labels_38PKT_25/source').ls(): 
    for img in Path('data/ref_landcovernet_v1_labels_38PKT_28/source').ls(): 
        print(img)
        if re.search('.*0101_B04_10m.tif', str(img)) : rgbnl['red'] = img 
        if re.search('.*0101_B03_10m.tif', str(img)) : rgbnl['green'] = img
        if re.search('.*0101_B02_10m.tif', str(img)) : rgbnl['blue'] = img
        if re.search('.*0101_B08_10m.tif', str(img)) : rgbnl['nir'] = img
    rgb = get_rgb(rgbnl)
    filename = 'rbd_testing'
    plt.imsave(filename + '.png', rgb.astype('uint8'))


