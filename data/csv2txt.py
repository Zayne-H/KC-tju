'''
功能：将csv文件中的实体提取出来作为字典

'''

import pandas as pd
df = pd.read_csv('./movie_title.csv')
title = df['movie_title'].values

with open('./movie_title.txt', 'a') as f:
    for t in title[1:]:
        f.write(t + ' ' + 'nz' + '\n')