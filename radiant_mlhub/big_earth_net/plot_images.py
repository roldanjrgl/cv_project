# ======================================================
# Plot images 
# ======================================================
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms


def plot_images(img):
    #plt.imshow(np.transpose(img, (1, 2, 0)))
    plt.imshow( tensor_image.permute(1, 2, 0)  )
    plt.show()

im = Image.open('data/S2B_MSIL2A_20170709T094029_30_50_B02.tif')
im.mode
im.convert('RGB')
print(im.size)
print(im.getdata())
data2 = np.array(im.getdata()).reshape(im.size[::-1])
#data2 = Image.Image.getdata(im)
print(data2.shape)
    
img = plt.imread('data/S2B_MSIL2A_20170709T094029_30_50_B02.tif')
img = img.astype(np.int32)   
print(img.shape)
tensored = torch.from_numpy(img)
print(tensored.shape)
plt.imshow(tensored)
plt.show()

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img=mpimg.imread('data/S2B_MSIL2A_20170709T094029_30_50_B02.tif')
imgplot = plt.imshow(img)
plt.colorbar()
plt.show()


imgplot = plt.imshow(img, clim=(200, 800))
plt.show()

plt.imshow(img, cmap="hot")
plt.show()


plt.imshow(img, cmap=plt.cm.prism)
plt.show()