# encoding=utf-8
'''
功能：将csv文件中的实体提取出来作为字典

'''

import pandas as pd
df = pd.read_csv('./conference.csv')
title = df['conference'].values

with open('./conference.txt', 'a') as f:
    for t in title[1:]:
        f.write(t + ' ' + 'pm' + '\n')