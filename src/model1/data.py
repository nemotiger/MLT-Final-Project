import sys
import pandas as pd

mode = sys.argv[1]
users_features_csv = sys.argv[2]
books_features_csv = sys.argv[3]
samples_csv = sys.argv[4]
output_file = sys.argv[5]

users = pd.read_csv(users_features_csv, index_col=0, header=0, dtype={'User-ID':str,'Country-lat':float,'Country-lng':float,'Age':float,'Privacy-Location':float,'Privacy-Age':float})
books = pd.read_csv(books_features_csv, index_col=0, header=0, dtype={'Index':str,'ISBN':str,'Book-Author':float,'Publisher':float,'Year-Of-Publication':float})
samples = pd.read_csv(samples_csv, header=0, dtype={'User-ID':str,'ISBN':str,'Book-Rating':float})

users = users[~users.index.duplicated(keep='first')] # remove rows with duplicated index
books = books[~books.index.duplicated(keep='first')] # remove rows with duplicated index

with open(output_file, 'w') as output:
    
    for row in samples.itertuples(index=False, name=None):
        if mode == 'train':
            uid, isbn, rating = row
        else:
            uid, isbn = row
        
        try:
            user = users.loc[uid].tolist()
        except KeyError:
            user = [-90.0, 0.0, 0.0, 2.0, 1.0]
        user = user[:-2] + [(user[-2]/2 + user[-1]) / 2]

        try:
            book = books.loc[isbn].tolist()
        except KeyError:
            book = [0.0, 0.0, 0.0, 2000.0]
        
        if mode == 'train':
            result = user + book + [rating]
        else:
            result = user + book
        
        result = [ str(r) for r in result ]
        output.write(' '.join(result) + '\n')