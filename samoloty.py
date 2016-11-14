from skimage import data, io
from skimage.morphology import disk
from skimage import filters
from skimage.filters import threshold_otsu
from pylab import *

paths = ['images/samolot01.jpg', 'images/samolot07.jpg', 'images/samolot08.jpg', 'images/samolot09.jpg', 'images/samolot10.jpg', 'images/samolot17.jpg']
images = []

#wczytywanie
for item in paths:
    images.append(data.imread(item, as_grey=True))

#modyfikacja obrazow
for i in range(len(images)):
    images[i] = filters.gaussian(images[i], 2).copy()
    images[i] = filters.median(images[i], disk(5))
    images[i] = filters.sobel(images[i])

    thresh = threshold_otsu(images[i])
    images[i] = (images[i] > thresh) * 255

figure(figsize=(20, 20))
y=231

#rysowanie
for i in range(len(images)):
    plt.subplot(y+i)
    plt.axis('off')
    io.imshow(images[i], cmap=plt.cm.gray)
    plt.savefig('myplot.jpg')
