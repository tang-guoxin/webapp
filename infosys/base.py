# -*- coding: utf-8 -*-
"""
Created on Sat May 14 09:55:34 2022

@author: tang
"""
import numpy as np
import pandas as pd
from .utils import InitTable


# %% 按条件查询
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
                             index=[i for i in range(1, len(ls) + 1)],
                             columns=['名称', '掌握程度'])
        return table


class SubWeight:
    def __init__(self, exam_names, *args):
        self.args = args
        self.exam_names = exam_names
        self.sub_score_ = self.get_sub_scores()
        self.sub_weight = self.get_weight(self.sub_score_)
        self.modele_score_ = self.get_module_scores()
        self.modele_weight = self.get_weight(self.modele_score_)

    def get_sub_scores(self):
        score = dict()
        for indc, exam_n in zip(self.args, self.exam_names):
            sub = indc['科目'].unique()
            d = dict()
            for s in sub:
                sco = InitTable.parsing_full_mark(
                    indc=indc,
                    reg={'模块': None, '科目': [s, ], '认知层次': None}
                )
                d[s] = sco
            score[exam_n] = d
        return score

    def get_module_scores(self):
        score = dict()
        for indc, exam_n in zip(self.args, self.exam_names):
            sub = indc['模块'].unique()
            d = dict()
            for s in sub:
                sco = InitTable.parsing_full_mark(
                    indc=indc,
                    reg={'模块': [s, ], '科目': None, '认知层次': None}
                )
                d[s] = sco
            score[exam_n] = d
        return score

    def get_weight(self, score):
        weight, key_s = dict(), list()
        for key, value in score.items():
            key_s.append(set(value.keys()))
        s0 = key_s[0]
        for s in key_s:
            s0 = s0 & s
        for s in s0:
            ls_ = list()
            for key, value in score.items():
                for k, v in value.items():
                    if s == k:
                        ls_.append(v)
            weight[s] = np.asarray(ls_) / sum(ls_)
        return weight

    def update(self, *args):
        table_1 = self.get_table('科目', self.sub_score_, self.sub_weight, *args)
        table_2 = self.get_table('模块', self.modele_score_, self.modele_weight, *args)
        return [table_1, table_2]

    def get_table(self, col, score, weight, *args):
        res = dict()
        for k in weight.keys():
            ls_ = list()
            for dic in args:
                ls_.append(dic[k]['掌握程度'])
            res[k] = np.sum(weight[k] * np.asarray(ls_))
        ukey = self.unique_set(score)
        ures = dict()
        for uk in ukey:
            for dic in args:
                if uk in dic.keys():
                    ures[uk] = dic[uk]['掌握程度']
        data_ls = list()
        for k, v in res.items():
            data_ls.append([k, v])
        # for k, v in ures.items():
        #     data_ls.append([k, v])
        return pd.DataFrame(
            data=data_ls,
            columns=['科目/模块', '掌握程度'],
            index=[i+1 for i in range(len(data_ls))]
        )

    def unique_set(self, score):
        unis, com = set(), list()
        for key, value in score.items():
            unis = unis.union(set(value.keys()))
            com.append(set(value.keys()))
        s0 = com[0]
        for c in com:
            s0 = s0 & c
        ukey = unis - s0
        return ukey

    def intersection_set(self, *args):
        res = set()
        for s in args:
            res = res.union(s)
        return res

    # 传入 update 的 res
    def totle_performance(self, dic_ls, *smtables):
        stable, mtable = smtables[0], smtables[1]
        sub = stable['科目/模块']
        mod = mtable['科目/模块']
        all_sub, all_mod = list(), list()
        for df in self.args:
            all_sub += list(df['科目'].unique())
            all_mod += list(df['模块'].unique())
        all_mod = list(set(all_mod))
        all_sub = list(set(all_sub))
        def chose_uniq(all_obj, ob):
            ret = list()
            for s in all_obj:
                for dic in dic_ls:
                    for k, v in dic.items():
                        if k == s and k not in list(ob):
                            ret.append([s, dic[k]['掌握程度']])
            return ret
        res_sub_table = chose_uniq(all_sub, sub)
        res_mod_table = chose_uniq(all_mod, mod)

        res_sub_table = pd.DataFrame(
            data=res_sub_table,
            columns=['科目/模块', '掌握程度']
        )
        res_mod_table = pd.DataFrame(
            data=res_mod_table,
            columns=['科目/模块', '掌握程度']
        )
        res_sub_table = res_sub_table.append(stable)
        res_sub_table = res_sub_table.reset_index(drop=True)

        res_mod_table = res_mod_table.append(mtable)
        res_mod_table = res_mod_table.reset_index(drop=True)

        return [res_sub_table, res_mod_table]




