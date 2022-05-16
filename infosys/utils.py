# -*- coding: utf-8 -*-
"""
Created on Sat May 14 09:55:49 2022

@author: tang
"""

import pandas as pd
import numpy as np

from .decorator import is_str_ls_


# %% 从一个可迭代对象中选择符合条件的元素
@is_str_ls_
def chose_element(ls, reg):
    res = list()
    for ite in ls:
        if reg in ite:
            res.append(ite)
    return res


def chose_any_element(ls, args):
    res = list()
    for reg in args:
        res += chose_element(ls, reg)
    return res


# %% 计算指标下的总分和平均分
def calc_indicators(table=None, ind_name=None):
    ss = table[ind_name].sum().sum()
    ave = table[ind_name].mean().sum()
    return [ss, ave]


# %% 解析满分表格
# def parsing_full_mark(indc, reg={'科目': None, '模块': None, '认知层次': None}):
#     for k, v in reg.items():
#         if k not in reg.keys() or v is None:
#             continue
#         indc = indc[indc[k].isin(reg[k])]
#     return indc['满分'].sum()


# %% 打包成字典
def set_dic(indc, table, module, *args, **kwgrs):
    dic, weight = dict(), None
    dic['内容'] = args[0]
    dic['总分'] = args[1]
    dic['平均分'] = args[2]
    dic['满分'] = args[3]
    if module in indc['科目'].unique():
        sub = indc[indc['科目'].isin(args[0][0]['科目'])]
        rc = sub['认知层次'].unique()
        ful = list()
        for r in rc:
            sco = InitTable.parsing_full_mark(indc, reg={'科目': args[0][0]['科目'], '模块': None, '认知层次': [r, ]})
            ful.append(sco)
        arr = np.asarray(ful)
        weight = arr / np.sum(arr)
        dic['权重'] = dict(zip(rc, weight.tolist()))
        real = weight * table[args[0][1]].mean()
        excp = weight * sub['满分']
        dic['掌握程度'] = real.sum() / excp.sum()
    elif module in indc['认知层次'].unique():
        pass
    else:
        dic['掌握程度'] = args[2] / args[3]
    return dic


# %% 将一个表格实例化
class InitTable:
    def __init__(self, data_path, ind_path, data_sheet=0, ind_sheet=0,
                 exam_name=None, *args, **kwargs):
        self.exam_name = exam_name
        self.table = pd.read_excel(data_path, sheet_name=data_sheet)
        self.indicators = pd.read_excel(ind_path, sheet_name=ind_sheet)
        self.module_names_ = self.indicators['模块'].unique()
        self.subj_names_ = self.indicators['科目'].unique()
        self.cognize_names_ = self.indicators['认知层次'].unique()

    def __info__(self):
        title = self.table.columns
        print(f'考试名称:\t{self.exam_name}')
        print('可用字段:\t', list(title))

    @staticmethod
    def parsing_full_mark(indc, reg=None):
        if reg is None:
            reg = {'科目': None, '模块': None, '认知层次': None}
        for k, v in reg.items():
            if k not in reg.keys() or v is None:
                continue
            indc = indc[indc[k].isin(reg[k])]
        return indc['满分'].sum()

    def parsing_module(self):
        title = self.table.columns
        kw = self.indicators['模块'].unique()
        dic = dict()
        for k in kw:
            idc = self.indicators[self.indicators['模块'] == k]
            names = list(idc['科目'].unique())
            id_k = chose_any_element(title, names)
            dic[k] = set_dic(self.indicators, self.table, k, [{'科目': names}, id_k],
                             *calc_indicators(self.table, id_k),
                             self.parsing_full_mark(self.indicators,
                                                    reg={'科目': None,
                                                         '模块': [k, ],
                                                         '认知层次': None}
                                                    )
                             )
        return dic

    def parsing_table(self):
        title = self.table.columns
        dic = dict()
        kw = self.indicators['科目'].unique()
        kw = np.append(kw, self.indicators['认知层次'].unique())
        is_r, name1, name2 = False, None, None
        for k in kw:
            if not is_r:
                name1, name2 = [k, ], None
            if k in self.indicators['认知层次'].unique():
                is_r = True
            if is_r:
                name1, name2 = None, [k, ]
            id_k = chose_element(title, k)
            dic[k] = set_dic(self.indicators, self.table, k, [{'科目': [k, ]}, id_k],
                             *calc_indicators(self.table, id_k),
                             self.parsing_full_mark(self.indicators,
                                                    reg={'科目': name1,
                                                         '模块': None,
                                                         '认知层次': name2}))
        return dic

    def parsing_cognize(self):
        title = self.table.columns
        kw = self.indicators['认知层次'].unique()
        dic = dict()
        for k in kw:
            id_k = chose_element(title, k)
            sub = self.indicators[self.indicators['认知层次'].isin([k, ])]
            sub_ = list(sub['科目'])
            dic[k] = set_dic(
                self.indicators, self.table, k, [{'科目': sub_}, id_k],
                *calc_indicators(self.table, id_k), self.parsing_full_mark(
                    self.indicators, reg={'科目': sub_, '模块': None, '认知层次': [k, ]}
                )
            )
        for m in self.indicators['模块'].unique():
            s = list(self.indicators[self.indicators['模块'].isin([m, ])]['科目'].unique())
            for k in kw:
                id_k = chose_element(title, k)
                id_k = chose_any_element(id_k, s)
                sub = self.indicators[self.indicators['认知层次'].isin([k, ])]
                sub = sub[sub['模块'].isin([m, ])]
                sub_ = list(sub['科目'])
                if not sub_:
                    continue
                dic[k][m] = set_dic(
                    self.indicators, self.table, k, [{'科目': sub_}, id_k],
                    *calc_indicators(self.table, id_k), self.parsing_full_mark(
                        self.indicators, reg={'科目': sub_, '模块': [m, ], '认知层次': [k, ]}
                    )
                )
        return dic

    def parsing_table_column(self):
        title = self.table.columns
        dic = dict()
        rc = self.indicators['认知层次'].unique()
        sub = self.indicators['科目'].unique()
        kw = chose_any_element(title, rc)
        for k in kw:
            for r in rc:
                if r in k:
                    for s in sub:
                        if s in k:
                            dic[k] = set_dic(
                                self.indicators, self.table, k, [{'科目': [s, ]}, [k, ]],
                                *calc_indicators(self.table, k),
                                self.parsing_full_mark(
                                    self.indicators,
                                    reg={'科目': [s, ], '模块': None, '认知层次': [r, ]}
                                )
                            )
        return dic

    def set_module_kv(self, indc, dic):
        modules = self.indicators['模块'].unique()
        for key in dic.keys():
            for module in modules:
                if key == module:
                    args = dic[key]['内容']
                    # sub = indc[indc['科目'].isin(args[0]['科目'])]
                    ful, real = list(), list()
                    for i, s in enumerate(args[0]['科目']):
                        sco = InitTable.parsing_full_mark(indc, reg={'科目': [s, ], '模块': [module, ], '认知层次': None})
                        rea = dic[s]['掌握程度']
                        ful.append(sco)
                        real.append(rea)
                    arr = np.asarray(ful)
                    weight = arr / np.sum(arr)
                    dic[key]['权重'] = list(weight)
                    real = np.sum(np.asarray(real) * weight)
                    # excp = 1 # weight * np.ones(len(args[0]['科目']))
                    dic[key]['掌握程度'] = real
        return dic

    def set_cognize_kv(self, indc, dic):
        modules = self.indicators['认知层次'].unique()
        for key in dic.keys():
            for module in modules:
                if key == module:
                    args = dic[key]['内容']
                    # sub = indc[indc['科目'].isin(args[0]['科目'])]
                    ful, real = list(), list()
                    for i, s in enumerate(args[0]['科目']):
                        sco = InitTable.parsing_full_mark(indc, reg={'科目': [s, ], '模块': None, '认知层次': [key, ]})
                        rea = dic[s]['掌握程度']
                        ful.append(sco)
                        real.append(rea)
                    arr = np.asarray(ful)
                    weight = arr / np.sum(arr)
                    dic[key]['权重'] = list(weight)
                    dic[key]['掌握程度'] = np.sum(np.asarray(real) * weight)
                    # 子分支
                    mk = self.indicators['模块'].unique()
                    for m in mk:
                        sub = self.indicators[self.indicators['认知层次'].isin([key, ])]
                        sub = sub[sub['模块'].isin([m, ])]
                        sub_ = list(sub['科目'])
                        if sub_:
                            args = dic[key][m]['内容']
                            ful, real = list(), list()
                            for i, s in enumerate(args[0]['科目']):
                                sco = InitTable.parsing_full_mark(indc, reg={'科目': [s, ], '模块': None, '认知层次': [key, ]})
                                rea = dic[s]['掌握程度']
                                ful.append(sco)
                                real.append(rea)
                            arr = np.asarray(ful)
                            weight = arr / np.sum(arr)
                            dic[key][m]['权重'] = list(weight)
                            dic[key][m]['掌握程度'] = np.sum(np.asarray(real) * weight)
        return dic

    def create_dict(self):
        dic1 = self.parsing_module()
        dic2 = self.parsing_table()
        dic3 = self.parsing_table_column()
        dic4 = self.parsing_cognize()
        dic = {**dic1, **dic2, **dic3, **dic4}
        dic = self.set_module_kv(self.indicators, dic)
        dic = self.set_cognize_kv(self.indicators, dic)
        return dic

# %%
