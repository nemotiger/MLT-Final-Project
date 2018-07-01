import sys, os
import pandas as pd
from PIL import Image

def getImages(imagedirs, extension='jpg'):
    for subdir in imagedirs:
        with os.scandir(subdir) as _dir:
            for entry in _dir:
                if not entry.name.startswith('.') and entry.name.endswith('.'+extension) and entry.is_file():
                    yield subdir, entry.name


book_csv = sys.argv[1]
images_dir = sys.argv[2]
result_csv = sys.argv[3]

subimage_dir = []
with os.scandir(images_dir) as _dir:
    for entry in _dir:
        if entry.is_dir():
            subimage_dir.append(images_dir + '/' + entry.name)

books = pd.read_csv(book_csv, index_col=0, usecols=['ISBN', 'Image-URL-L'], dtype={'ISBN':str, 'Image-URL-L':str})

result = {'ISBN' : [], 'URL' : [], 'PATH' : []}
count = 0
for _dir, image in getImages(subimage_dir):
    try:
        img = Image.open(_dir + '/' + image)
        img = img.load()
    except KeyboardInterrupt:
        print('KeyboardInterrupt...exit.')
        sys.exit(0)
    except:
        isbn = image[:-4]
        result['ISBN'].append(isbn)
        result['URL'].append(books.loc[isbn, 'Image-URL-L'])
        result['PATH'].append(_dir + '/' + image)
        count += 1
        print('{} bad images found. Image: {}'.format(count, image))

result = pd.DataFrame(result)
result.to_csv(result_csv, index=False)

