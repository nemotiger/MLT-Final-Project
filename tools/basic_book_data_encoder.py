import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


book_csv = sys.argv[1]
output_csv = sys.argv[2]

features = ['ISBN','Book-Author','Year-Of-Publication','Publisher']

books = pd.read_csv(book_csv, usecols=features)
books.set_index('ISBN', drop=False, inplace=True)

trans = { feature : LabelEncoder().fit_transform(books[feature].astype(str)) for feature in features if feature != 'Year-Of-Publication' }
trans['Year-Of-Publication'] = books['Year-Of-Publication']

result = pd.DataFrame(trans, index=books.index, dtype=np.float64)
result.index.name = 'Index'
result.to_csv(output_csv)