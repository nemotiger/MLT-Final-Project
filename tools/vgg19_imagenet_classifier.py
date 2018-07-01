import sys, os
import csv
import numpy as np
from keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array


def getImages(imagedir, extension='jpg'):
    with os.scandir(imagedir) as _dir:
        for entry in _dir:
            if not entry.name.startswith('.') and entry.name.endswith('.'+extension) and entry.is_file():
                yield entry.name



image_dir = sys.argv[1]
output_csv = sys.argv[2]

# load model
model = VGG19()

with open(output_csv, 'w', newline='') as result_csv:

    result_writer = csv.writer(result_csv, quoting=csv.QUOTE_MINIMAL)
    result_writer.writerow(['ISBN', 'Class'])

    isbn = []
    images = []

    for name in getImages(image_dir):
        image = load_img(name, target_size=(224, 224))
        image = img_to_array(image)
        images.append(np.expand_dims(image, axis=0))
        isbn.append(name[:-4])

    images = np.concatenate(images, axis=0)
    images = preprocess_input(images)
    pred = model.predict(images)
    labels = decode_predictions(pred)

    labels = [ label[0][1] for label in labels ]
    label_to_class = { l : float(i) for i, l in enumerate(set(labels)) }

    for book_isbn, label in zip(isbn, labels):
        result_writer.writerow([book_isbn, label_to_class[label]])
