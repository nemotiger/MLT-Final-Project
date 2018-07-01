import sys, os
import pandas as pd
import numpy as np
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


def getImages(imagedirs, extension='jpg'):
    for subdir in imagedirs:
        with os.scandir(subdir) as _dir:
            for entry in _dir:
                if not entry.name.startswith('.') and entry.name.endswith('.'+extension) and entry.is_file():
                    yield subdir, entry.name



images_dir = sys.argv[1]
output_csv = sys.argv[2]

subimage_dir = []
with os.scandir(images_dir) as _dir:
    for entry in _dir:
        if entry.is_dir():
            subimage_dir.append(images_dir + '/' + entry.name)

print('Loading Images')

images = []
isbn = []
count = 0
for _dir, img in getImages(subimage_dir):
    try:
        with Image.open(_dir + '/' + img) as image:
            if image.size == (1,1): # empty image
                continue
        image = load_img(_dir + '/' + img, target_size=(100, 62))
        image = img_to_array(image).flatten()
        images.append(np.expand_dims(image, axis=0))
        isbn.append(img[:-4])
        count += 1
        if count % 1000 == 0:
            print('{} images loaded'.format(count))
        
    except OSError:
        pass

images = np.concatenate(images, axis=0)

print('Writing loaded images to imgarray.npy')
np.save('imgarray.npy', images)

print('Start PCA')
pca = PCA(n_components=0.8, svd_solver='full')
images = pca.fit_transform(images)
print('PCA n_component: {}'.format(pca.n_components_))

print('Start KMeans clustering')
kmeans = KMeans(n_clusters=100, verbose=True, n_jobs=8).fit(images)
cluster = kmeans.predict(images)

print('Clustering done. Writing results to {}'.format(output_csv))
result = pd.DataFrame({'ISBN':isbn, 'Image-Class':cluster})
result.to_csv(output_csv, index=False)