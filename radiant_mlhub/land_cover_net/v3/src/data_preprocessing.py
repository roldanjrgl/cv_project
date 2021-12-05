import numpy
from fastai.vision.all import *
from numpy.lib.utils import source
import rasterio as rio
import os 

def convert_source_to_png(source_day, bands, source_day_dir):
    # all_rgb_bands =  ('B04' in bands) and ('BO3' in bands) and ('BO2' in bands)
    all_rgb_bands =  'B04' in bands and 'B03' in bands and 'B02' in bands 
    if all_rgb_bands:
        red = rio.open(bands['B04']).read(1) 
        green = rio.open(bands['B03']).read(1) 
        blue = rio.open(bands['B02']).read(1) 
    else:
        return
    
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
    # bands_for_image_chip_labels = {}
    # for label_path in Path(image_chip_path/f'labels').ls():
    #     label_name = str(source_day)[-29:-21]
    #     bands_for_image_chip_labels[label_name] = label_path

    return bands_for_image_chip_source_day

def convert_all_sources_to_png(all_source_path):
    data_png_path = '../data_png'

    if os.path.isdir(data_png_path) == False:
        os.mkdir(data_png_path)
    
    for image_chip_path in Path(all_source_path).ls():
        print(image_chip_path)

        bands_for_image_chip_source_day = classify_bands_for_one_image_chip(image_chip_path)
        convert_all_source_days_for_image_chip(bands_for_image_chip_source_day, data_png_path)

def convert_label_to_png(image_chip_label_path, data_png_path, image_chip_name):
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
    data_png_path = '../data_png'

    if os.path.isdir(data_png_path) == False:
        os.mkdir(data_png_path)
    
    for image_chip_path in Path(data_png_path).ls():
        print(image_chip_path)
        image_chip_name = str(image_chip_path)[-8:]
        print(image_chip_name)

        image_chip_label_name = all_labels_path.split('/')[2] + '_' + image_chip_name
        print(image_chip_label_name)
        
        image_chip_label_path =  all_labels_path + '/' + image_chip_label_name + '/' + 'labels.tif'
        print(image_chip_label_path)

        convert_label_to_png(image_chip_label_path, data_png_path, image_chip_name)

        

        

