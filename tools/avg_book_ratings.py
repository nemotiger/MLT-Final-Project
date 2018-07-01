import sys
import pandas as pd
import numpy as np

ratings_csv = sys.argv[1]
output_csv = sys.argv[2]

ratings = pd.read_csv(ratings_csv, index_col=0, usecols=['ISBN','Book-Rating'], dtype={'ISBN':str, 'Book-Rating':float})

avg_all = np.rint(ratings['Book-Rating'].mean())
result = ratings.groupby(ratings.index)['Book-Rating'].mean().round()
result = result.append(pd.Series([avg_all], index=['avg']))
result = result.to_frame()
result.columns = ['Book-Rating']
result.index.name = 'ISBN'
result.to_csv(output_csv)