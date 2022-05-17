import streamlit as st
import pandas as pd
import numpy as np
from infosys.utils import InitTable
import altair as alt
from infosys.base import QuaryInfo
from infosys.base import SubWeight

# from bokeh.plotting import figure
import altair as alt

st.title('基本检索')

obj_1 = InitTable(data_path='./data/2021水平测试.xlsx',
                  ind_path='./data/2021水平测试满分.xlsx', exam_name='水平测试')
obj_2 = InitTable(data_path='./data/2021经典数据.xlsx', data_sheet='二级',
                  ind_path='./data/2021经典满分.xlsx', exam_name='经典考试')

module_check_1 = list()
sub_check_1 = list()
cog_check_1 = list()
module_check_2 = list()
sub_check_2 = list()
cog_check_2 = list()


def set_options(val=False):
    col_1, col_2 = st.columns(2)
    with col_1:
        st.header(obj_1.exam_name)
        st.subheader('模块名')
        for n in obj_1.module_names_:
            module_check_1.append(st.checkbox(label=n, value=val, key=n + 'obj1'))
        st.subheader('科目')
        for n in obj_1.subj_names_:
            sub_check_1.append(st.checkbox(label=n, value=val, key=n + 'obj1'))
        st.subheader('认知层次')
        for n in obj_1.cognize_names_:
            cog_check_1.append(st.checkbox(label=n, value=val, key=n + 'obj1'))
    with col_2:
        st.header(obj_2.exam_name)
        st.subheader('模块名')
        for n in obj_2.module_names_:
            module_check_2.append(st.checkbox(label=n, value=val, key=n + 'obj2'))
        st.subheader('科目')
        for n in obj_2.subj_names_:
            sub_check_2.append(st.checkbox(label=n, value=val, key=n + 'obj2'))
        st.subheader('认知层次')
        for n in obj_2.cognize_names_:
            cog_check_2.append(st.checkbox(label=n, value=val, key=n + 'obj2'))


def is_none(dic: dict):
    for k, v in dic.items():
        if v is not None:
            return True
    return False


with st.sidebar:
    set_options()
    with st.spinner("Loading..."):
        click = st.button(label='开始')
        st.success("Done!")

if st.checkbox('显示数据字典'):
    col_1, col_2 = st.columns(2)
    with col_1:
        st.header('水平测试')
        d_1 = obj_1.create_dict()
        st.write(d_1)
    with col_2:
        st.header('经典考试')
        d_2 = obj_2.create_dict()
        st.write(d_2)


def run():
    reg_1, reg_2 = dict(), dict()
    reg_1['模块名'] = None if sum(module_check_1) == 0 else obj_1.module_names_[module_check_1].tolist()
    reg_1['科目'] = None if sum(sub_check_1) == 0 else obj_1.subj_names_[sub_check_1].tolist()
    reg_1['认知层次'] = None if sum(cog_check_1) == 0 else obj_1.cognize_names_[cog_check_1].tolist()

    reg_2['模块名'] = None if sum(module_check_2) == 0 else obj_2.module_names_[module_check_2].tolist()
    reg_2['科目'] = None if sum(sub_check_2) == 0 else obj_2.subj_names_[sub_check_2].tolist()
    reg_2['认知层次'] = None if sum(cog_check_2) == 0 else obj_2.cognize_names_[cog_check_2].tolist()

    sw = SubWeight([obj_1.exam_name, obj_2.exam_name], obj_1.indicators, obj_2.indicators)
    tables = sw.update(obj_1.create_dict(), obj_2.create_dict())
    sub_score_ = sw.sub_score_
    modele_score_ = sw.modele_score_
    col_1, col_2 = st.columns(2)
    qr_1 = QuaryInfo(obj_1.create_dict())
    qr_2 = QuaryInfo(obj_2.create_dict())
    with col_1:
        dic_1_ = sub_score_[obj_1.exam_name]
        dic_2_ = modele_score_[obj_1.exam_name]
        if not is_none(reg_1):
            st.warning('No options.')
        else:
            st.header('水平测试')
            st.table(qr_1.update(reg_1))
            st.subheader('具有共同科目的总体情况')
            st.table(tables[0])
            df = pd.DataFrame(
                {'科目': dic_1_.keys(), '分数': dic_1_.values()}
            )
            df_2 = pd.DataFrame(
                {'模块': dic_2_.keys(), '分数': dic_2_.values()}
            )
            c1 = alt.Chart(df).mark_bar().encode(x='科目', y='分数')
            c2 = alt.Chart(df_2).mark_bar().encode(x='模块', y='分数')
            st.subheader('科目分数占比')
            st.altair_chart(c1)
            st.subheader('模块分数占比')
            st.altair_chart(c2)
    with col_2:
        dic_1_ = sub_score_[obj_2.exam_name]
        dic_2_ = modele_score_[obj_2.exam_name]
        if not is_none(reg_2):
            st.warning('No options.')
        else:
            st.header('经典考试')
            st.table(qr_2.update(reg_2))
            st.subheader('具有共同模块的总体情况')
            st.table(tables[1])
            df = pd.DataFrame(
                {'科目': dic_1_.keys(), '分数': dic_1_.values()}
            )
            df_2 = pd.DataFrame(
                {'模块': dic_2_.keys(), '分数': dic_2_.values()}
            )
            c1 = alt.Chart(df).mark_bar().encode(x='科目', y='分数')
            c2 = alt.Chart(df_2).mark_bar().encode(x='模块', y='分数')
            st.subheader('科目分数占比')
            st.altair_chart(c1)
            st.subheader('模块分数占比')
            st.altair_chart(c2)

if click:
    run()
