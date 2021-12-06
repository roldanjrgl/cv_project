import numpy as np
from fastai.vision.all import *
from numpy.lib.utils import source
# import rasterio as rio
import os 
import cv2
import matplotlib.pyplot as plt

def convert_mask_to_rgb(mask):
    # class_to_rgb = {
    #          0: (80,0,165),
    #          1: (255,204,0),
    #          2: (0,244,244),
    #          3: (105,105,105)}    

    class_to_rgb = {
             1: (80,0,165),
             2: (255,204,0),
             3: (0,244,244),
             4: (105,105,105)}    


    red = np.zeros_like(mask)
    green = np.zeros_like(mask)
    blue = np.zeros_like(mask)
    
    num_classes = 4
    h, w = mask.shape[0], mask.shape[1]
    for row in range(h):
        for col in range(w):
            for class_idx in range(1, num_classes + 1):
                if mask[row][col] == class_idx:
                    red[row][col] = class_to_rgb[class_idx][0]
                    green[row][col] = class_to_rgb[class_idx][1]
                    blue[row][col] = class_to_rgb[class_idx][2]
            

    rgb = np.dstack((red, green, blue))
    return rgb

def convert_all_masks_to_png(all_masks_path):
    for image_chip_path in Path(data_png_path).ls():
        print(image_chip_path)


def main():
    # label_to_path = 'M-33-20-D-c-4-2.tif'
    # label = rio.open(label_to_path)
    # mask = label.read(1) 
    # plt.imsave('labels' + '.png', mask.astype('uint8'))

    # example
    label_path = 'M-33-20-D-c-4-2_0_m.png'
    img = cv2.imread(label_path,0)
    print('END OF FILE')
    mask_rgb = convert_mask_to_rgb(img)

    plt.imsave('mask_rgb' + '.png', mask_rgb.astype('uint8'))

    #
    # all_masks_path = '../../../../data_sources/landcover.ai.v1/output'
    # convert_all_masks_to_png(all_masks_path)




if __name__ == "__main__":
    main()