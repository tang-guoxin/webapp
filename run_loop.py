# -*- coding: utf-8 -*-
"""
Created on Sat May 14 09:53:56 2022

@author: tang
"""

import pandas as pd
from infosys.utils import InitTable

# table = pd.read_excel('./data/2021水平测试.xlsx')

obj_1 = InitTable(data_path='./data/2021水平测试.xlsx',
                  ind_path='./data/2021水平测试满分.xlsx', exam_name='水平测试')

obj_2 = InitTable(data_path='./data/2021经典数据.xlsx', data_sheet='二级',
                  ind_path='./data/2021经典满分.xlsx', exam_name='经典考试')

d = obj_2.create_dict()

# print(d)
print('=='*100)
for i, (k, v) in enumerate(d.items()):
    print(i+1, '\t', k, ':\t', v)
    print()

print('=='*100)


from infosys.base import QuaryInfo

qr = QuaryInfo(dic=d)

reg = {'模块名': ['中医基础', '医学人文'], '科目': ['中基', '伤寒'], '认知层次': ['记忆']}
# reg = {'模块名': None, '科目': ['中基', '伤寒'], '认知层次': None}
# reg = {'模块名': ['中医基础', '医学人文'], '科目': None, '认知层次': None}
# reg = {'模块名': None, '科目': None, '认知层次': ['记忆', '理解']}

res = qr.update(reg)
print(res)

# for r_ in res:
#     print(r_)
