import sys
import pandas as pd

implicit_csv = sys.argv[1]
avg_ratings_csv = sys.argv[2]
output_csv = sys.argv[3]

implicit = pd.read_csv(implicit_csv, usecols=['ISBN', 'User-ID'], dtype={'User-ID':str,'ISBN':str})
avg_ratings = pd.read_csv(avg_ratings_csv, index_col=0, dtype={'ISBN':str,'Book-Rating':float})

ratings = []
for isbn in implicit['ISBN']:
    try:
        ratings.append(avg_ratings.loc[isbn, 'Book-Rating'])
    except KeyError:
        ratings.append(avg_ratings.loc['avg', 'Book-Rating'])

result = pd.DataFrame({ 'User-ID' : implicit['User-ID'], 'ISBN' : implicit['ISBN'], 'Book-Rating' : ratings })
result.to_csv(output_csv, index=False)