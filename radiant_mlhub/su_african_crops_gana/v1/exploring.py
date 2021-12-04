import rasterio as rio
from preprocessing import * 
from plotting import * 

def explore_dataset():
    # label_v1 = rio.open('labels.tif')
    # label = rio.open('labels.tif').read(1)
    # plt.imsave('label_testing' + '.png', label)

    # ===================================
    # explore labels.tif files
    # ===================================
    dataset = rio.open('labels.tif')
    print(dataset.name)
    print(dataset.mode)
    print(dataset.count)
    print(dataset.indexes)
    band1 = dataset.read(1)
    print(type(band1))
    print(band1)

    # ===================================
    # plot_label(band1)
    # ===================================
    # plot_label_legends(band1)


    # ===================================
    # plot_source
    # ===================================
    data_source_path = 'data/su_african_crops_ghana_source_s2_000000_2016_01_13/source.tif'
    source = rio.open(data_source_path)
    print(f'source indexes = {source.indexes}')
    source_bands = source.read(1)
    convert_source_to_png(data_source_path, 'source_v2')

    # ===================================
    # plot_cloud_mask
    # ===================================
    cloud_mask_path = 'data/su_african_crops_ghana_source_s2_000000_2016_01_13/cloudmask.tif'
    cloud_mask = rio.open(cloud_mask_path)
    print(f'cloud_masks indexes = {cloud_mask.indexes}')
    cloud_mask_bands = cloud_mask.read(1)
    # convert_source_to_png(cloud_mask_path, 'cloudmask')
    plot_label_legends(cloud_mask_bands)