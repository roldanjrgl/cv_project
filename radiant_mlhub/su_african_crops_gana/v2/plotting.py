import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


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