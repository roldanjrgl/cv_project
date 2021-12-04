import numpy
from fastai.vision.all import *
from numpy.lib.utils import source
import rasterio as rio
import os 

def get_source_rgb(path_dict):
    # reference_got_from:  https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    red = rio.open(path_dict['red']).read(1) # B4
    green = rio.open(path_dict['green']).read(1) # B3
    blue = rio.open(path_dict['blue']).read(1) # B2

    rgb = np.dstack((red, green, blue))

    # normalize and convert to range 0-255
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    return rgb

# def convert_source_to_png(data_in_path, data_out_path):
#     # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
#     rgbnl = {}
#     for img in Path('data/ref_landcovernet_v1_labels_38PKT_29/source').ls(): 
#         print(img)
#         if re.search('.*0101_B04_10m.tif', str(img)) : rgbnl['red'] = img 
#         if re.search('.*0101_B03_10m.tif', str(img)) : rgbnl['green'] = img
#         if re.search('.*0101_B02_10m.tif', str(img)) : rgbnl['blue'] = img
#         if re.search('.*0101_B08_10m.tif', str(img)) : rgbnl['nir'] = img
#     rgb = get_source_rgb(rgbnl)
#     filename = 'rbd_testing'
#     plt.imsave(filename + '.png', rgb.astype('uint8'))

# def convert_source_to_png(data_in_path, data_out_path):
#     # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
#     rgbnl = {}
#     for img in Path(data_in_path).ls(): 
#         print(img)
#         if re.search('.*0101_B04_10m.tif', str(img)) : rgbnl['red'] = img 
#         if re.search('.*0101_B03_10m.tif', str(img)) : rgbnl['green'] = img
#         if re.search('.*0101_B02_10m.tif', str(img)) : rgbnl['blue'] = img
#         if re.search('.*0101_B08_10m.tif', str(img)) : rgbnl['nir'] = img
#     rgb = get_source_rgb(rgbnl)
#     filename = 'rbd_testing'
#     plt.imsave(data_out_path + '.png', rgb.astype('uint8'))


def get_label(path_dict):
    # reference_got_from:  https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    channel = rio.open(path_dict['band']).read(1)

    # rgb = np.dstack((red, green, blue))

    # normalize and convert to range 0-255
    channel_normalized = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype(int)
    return channel_normalized 


def convert_label_to_png(path_to_label):
    # refence_based_on: https://github.com/pavlo-seimskyi/semantic-segmentation-satellite-imagery/blob/main/download_data.ipynb
    label_img = {}
    # for img in Path('data/ref_landcovernet_v1_labels_38PKT_29/labels').ls(): 
    for img in Path(path_to_label).ls(): 
        print(img)
        if re.search('labels.tif', str(img)) : label_img['band'] = img 

    label = rio.open(label_img['band']).read(1)
    # rgb = get_label(rgbnl)

    # filename = 'label_testing'
    label_png_folder = 'data_labels_png'
    
    if os.path.isdir(label_png_folder) == False:
        os.mkdir(label_png_folder)
    
    # plt.imsave(label_png_folder +  path_to_label[-36:] + '.png', label.astype('uint8'))
    plt.imsave(label_png_folder +  path_to_label[-36:] + '.png', label)



def convert_all_labels_to_png(all_labels_path):
    for path_to_label in Path(all_labels_path).ls():
        path_to_label_str = str(path_to_label)
        if path_to_label_str != 'data_all_labels/ref_landcovernet_v1_labels/.DS_Store':
            convert_label_to_png(path_to_label_str)


def classify_bands_for_one_image_chip(image_chip_path):
    # classify source images
    bands_for_image_chip_source_day = {}
    for source_day in Path(image_chip_path/f'source').ls():
        source_day_name = str(source_day)[-29:-12]
        band = str(source_day)[-11:-8]
        # sample_source_day[source_day_name][band] = source_day
        if (source_day_name in bands_for_image_chip_source_day.keys()):
            bands_for_image_chip_source_day[source_day_name][band] = source_day
        else:
            bands_for_image_chip_source_day[source_day_name] = {}
            bands_for_image_chip_source_day[source_day_name][band] = source_day
        print(source_day)
        print(source_day_name)
        print(band)

    # classify labels 
    bands_for_image_chip_labels = {}
    for label_path in Path(image_chip_path/f'labels').ls():
        label_name = str(source_day)[-29:-21]
        bands_for_image_chip_labels[label_name] = label_path

    return bands_for_image_chip_source_day, bands_for_image_chip_labels


def convert_source_to_png(source_day, bands, source_day_dir):
    red = rio.open(bands['B04']).read(1) 
    green = rio.open(bands['B03']).read(1) 
    blue = rio.open(bands['B02']).read(1) 
    
    rgb = np.dstack((red, green, blue))
    rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min()) * 255).astype(int)
    plt.imsave(source_day_dir + '/' +  source_day + '.png', rgb.astype('uint8'))


def convert_all_source_days_for_image_chip(bands_for_image_chip_source_day, data_png_path):
    for source_day, bands  in bands_for_image_chip_source_day.items():
        print(source_day)
        print(bands)

        source_day_dir = data_png_path + '/' + source_day[:8]
        if os.path.isdir(source_day_dir) == False:
            os.mkdir(source_day_dir)
        
        # source_day_dir.append('/source')
        source_day_dir  = source_day_dir + '/source'
        if os.path.isdir(source_day_dir) == False:
            os.mkdir(source_day_dir)

        convert_source_to_png(source_day, bands, source_day_dir)


def convert_label_to_png(label, bands, label_dir):
    channel = rio.open(str(bands)).read(1)

    channel_normalized = ((channel - channel.min()) / (channel.max() - channel.min()) * 255).astype(int)
    plt.imsave(label_dir + '/' +  label + '.png', channel_normalized.astype('uint8'))




def convert_all_labels_for_image_chip(bands_for_image_chip_labels, data_png_path):
    bands_for_image_chip_labels
    for label, bands in bands_for_image_chip_labels.items():
        print(label)
        print(bands)

        label_dir = data_png_path + '/' + label[:8]
        # label_dir = data_png_path + '/label'
        if os.path.isdir(label_dir) == False:
            os.mkdir(label_dir)

        label_dir = label_dir + '/label'
        if os.path.isdir(label_dir) == False:
            os.mkdir(label_dir)

        convert_label_to_png(label, bands, label_dir)


def convert_data_to_png(data_path):
    # if folder for data_png doesn't exist, create one
    data_png_path = 'data_png'
    if os.path.isdir(data_png_path) == False:
        os.mkdir(data_png_path)

    for image_chip_path in Path(data_path).ls():
        sample_name = str(image_chip_path)[5:]
        # print(sample_path)
        # print(sample_path/f'source')
        # print(sample_path/f'labels')
        # convert_source_to_png(sample_path/f'source', data_png_path / sample_name / )

        bands_for_image_chip_source_day, bands_for_image_chip_labels = classify_bands_for_one_image_chip(image_chip_path)
        convert_all_source_days_for_image_chip(bands_for_image_chip_source_day, data_png_path)
        convert_all_labels_for_image_chip(bands_for_image_chip_labels, data_png_path)


    print('END OF FUNCT')