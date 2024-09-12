'''
功能：将csv文件中的实体提取出来作为字典

'''

import pandas as pd
df = pd.read_csv('./person.csv')
title = df['person'].values

with open('./person.txt', 'a') as f:
    for t in title[1:]:
        f.write(t + ' ' + 'pp' + '\n')