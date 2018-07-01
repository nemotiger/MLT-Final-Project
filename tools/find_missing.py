import sys, os
import csv

books_csv = sys.argv[1] # books.csv
images_dir = sys.argv[2]
result_csv = sys.argv[3]

exist_images = set()
with os.scandir(images_dir) as _dir:
    for entry in _dir:
        if entry.is_dir():
            exist_images.update(os.listdir(images_dir + '/' + entry.name))

with open(books_csv, 'r', newline='') as books, \
    open(result_csv, 'w', newline='') as result:

    books_reader = csv.reader(books)
    result_writer = csv.writer(result)

    # remove header
    next(books_reader)

    # write header
    result_writer.writerow(['ISBN', 'URL'])

    count = 0

    for book in books_reader:
        isbn = book[0]
        image_url = book[7]

        if isbn+'.jpg' not in exist_images:
            result_writer.writerow([isbn, image_url])
            count += 1
            print('{} missing images found. Image: {}'.format(count, isbn+'.jpg'))

