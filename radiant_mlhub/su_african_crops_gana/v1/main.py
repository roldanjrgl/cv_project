import os
from matplotlib.colors import Colormap
import rasterio as rio
from fastai.vision.all import *
import matplotlib.patches as mpatches

os.environ['MLHUB_API_KEY'] = '688769cc570be590e2cf107b8418eab0aba12eb23a0a29069b06b870d6c38049'

def plot_label(label):
    plt.imshow(label,cmap='tab20')
    plt.colorbar(label)
    plt.show()
    plt.legend()
    

def plot_label_legends(label):
    # reference_based_on: https://stackoverflow.com/questions/25482876/how-to-add-legend-to-imshow-in-matplotlib
    data = label

    plt.figure(figsize=(8,4))
    im = plt.imshow(data, interpolation='none')
    values = np.unique(data.ravel())

    # get the colors of the values, according to the 
    # colormap used by imshow
    colors = [ im.cmap(im.norm(value)) for value in values]
    # create a patch (proxy artist) for every color 
    patches = [ mpatches.Patch(color=colors[i], label="Class {l}".format(l=int(values[i])) ) for i in range(len(values)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

    plt.show()

def main():
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
    plot_label_legends(band1)


    # ===================================
    # plot_source
    # ===================================




if __name__ == "__main__":
    main()