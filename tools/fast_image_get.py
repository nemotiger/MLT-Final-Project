import sys
import csv
import requests

input_csv = sys.argv[1] # books.csv
output_dir = sys.argv[2]
begin_idx = int(sys.argv[3])

with open(input_csv, 'r', newline='') as books_csv, \
    requests.Session() as session:

    books_reader = csv.reader(books_csv)

    # remove header
    next(books_reader)

    count = begin_idx
    for i in range(count):
        next(books_reader)

    for book in books_reader:
        isbn = book[0]
        output_file = output_dir + '/' + isbn + '.jpg'
        image_url = book[7] # Image-URL-L

        while True:
            try:
                r = session.get(image_url)
                break
            except requests.exceptions.ConnectionError:
                pass

        with open(output_file, 'wb') as output:
            output.write(r.content)

        count += 1
        print('{} images downloaded. Image: {}'.format(count, output_file))
