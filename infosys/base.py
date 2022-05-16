# -*- coding: utf-8 -*-
"""
Created on Sat May 14 09:55:34 2022

@author: tang
"""
import pandas as pd


class QuaryInfo:
    def __init__(self, dic):
        self.dic = dic

    def update(self, reg: dict):
        res = list()
        if (reg['认知层次'] is None or '认知层次' not in reg.keys()) and (reg['模块名'] is None or '模块名' not in reg.keys()):
            res = self.chose_val('科目', reg)
            return self.list2table(res)
        if (reg['认知层次'] is None or '认知层次' not in reg.keys()) and (reg['科目'] is None or '科目' not in reg.keys()):
            res = self.chose_val('模块名', reg)
            return self.list2table(res)
        if (reg['模块名'] is None or '模块名' not in reg.keys()) and (reg['科目'] is None or '科目' not in reg.keys()):
            res = self.chose_val('认知层次', reg)
            return self.list2table(res)
        temp_ = list()
        for k, v in reg.items():
            if v is None:
                continue
            temp_ += self.chose_val(k, reg)
        for t_ in temp_:
            if t_ not in res:
                res.append(t_)
        return self.list2table(res)

    def chose_val(self, name, reg):
        res = list()
        for k in reg[name]:
            res.append([k, self.dic[k]['掌握程度']])
            com = self.dic[k]['内容'][1]
            for c in com:
                res.append([c, self.dic[c]['掌握程度']])
        return res

    def list2table(self, ls):
        table = pd.DataFrame(data=ls,
                             index=[i for i in range(1, len(ls)+1)],
                             columns=['名称', '掌握程度'])
        return table
