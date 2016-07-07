from shared.myhbase import Myhbase
import numpy as np
import pandas as pd

class Myipython(Myhbase):

    def __init__(self):
        pass

    def categorytrend(self, category):

        print('Get trend data..')
        hb = Myhbase('trend')

        X = []
        Y = []
        if category is not '':

            try:
                hb = Myhbase('trend')
                i = 1
                rowkey = category + 'interests'

                for key, data in hb.table.scan(row_prefix=rowkey, ):
                    X.append([i])
                    v = int(data['stats:value'])
                    Y.append([v])
                    i += 1

            except:
                print('err')

            return(X, Y)

    def reject_outliers(data, m=2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d / mdev if mdev else 0.
        return data[s < m]


    def load_file(self, url):
        data = pd.read_csv(url)
        return data


# new_x = np.reshape(new_x, (563,1))
# In [50]: df[df.x_square > 0]
# pd.scatter_matrix(df, diagonal="kde", figsize=(10,10));

#
# In [68]: def f(x):
#    ....:     if x == 'NaN':
#    ....:         return 0
#    ....:     else:
#    ....:         return x
#    ....:
#
# In [69]: df['new'] = df['x_factorial].apply(f)
#   File "<ipython-input-69-196b2ec5cd7e>", line 1
#     df['new'] = df['x_factorial].apply(f)
#                                         ^
# SyntaxError: EOL while scanning string literal
#
#
# In [70]: df['new'] = df['x_factorial'].apply(f)
# In [1]: from myipython import Myipython
# In [2]: ip = Myipython()

# pd.to_csv
# import json
# json.load()
# pd.read_table
# pd .read_fwd
# col[np.abs(col)>3]
# data[(np.abs(data) > 3).any(1)]

