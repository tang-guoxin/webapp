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

# obj_3 = InitTable(data_path='./data/2018医考认知层次得分标准化150.xlsx',
#                   ind_path='./data/2018医考认知层次满分.xlsx', exam_name='医考')


d_1 = obj_1.create_dict()
d_2 = obj_2.create_dict()
# d_3 = obj_3.create_dict()

d = obj_1.create_dict()

# print(d)
print('=='*100)
for i, (k, v) in enumerate(d_2.items()):
    print(i+1, '\t', k, ':\t', v)
    print()

print('=='*100)


from infosys.base import QuaryInfo
from infosys.base import SubWeight

qr = QuaryInfo(dic=d)

reg = {'模块名': ['中医基础', '医学人文'], '科目': ['中基', '伤寒'], '认知层次': ['记忆']}
# reg = {'模块名': None, '科目': ['中基', '伤寒'], '认知层次': None}
# reg = {'模块名': ['中医基础', '医学人文'], '科目': None, '认知层次': None}
# reg = {'模块名': None, '科目': None, '认知层次': ['记忆', '理解']}

res = qr.update(reg)
print(res)

sw = SubWeight([obj_1.exam_name, obj_2.exam_name], obj_1.indicators, obj_2.indicators)
# sw = SubWeight([obj_1.exam_name, ], obj_1.indicators)
wt = sw.update(d_1, d_2)

print(wt)

print(sw.modele_score_)
print(sw.modele_weight)
# for r_ in res:
#     print(r_)
