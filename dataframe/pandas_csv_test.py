import pandas as pd
import csv
from pandas import read_csv, ExcelWriter
import re
from openpyxl import Workbook
import datetime


def create_first_df():
    df1 = read_csv('../av_by_parser_test.csv')
    df2 = read_csv('../bamper_parser.csv')
    df_re = df1.append(df2)
    reverse_date = []
    for i in range(0, len(df_re)):
        datetime = df_re.iloc[i]['Дата публикации']
        datetime_reverse = str(datetime)[3:6] + str(datetime)[:3] + str(datetime)[6:]
        reverse_date.append(datetime_reverse)
    df_re['Дата публикации'] = reverse_date
    df_re['Дата публикации'] = pd.to_datetime(df_re['Дата публикации'])
    with pd.ExcelWriter('factoring/df_re.xlsx') as writer:
        df_re.to_excel(writer, sheet_name='try')
    df_res1 = df_re.loc[df_re['Цена'] < 450]
    df_res1 = df_res1.loc[df_res1['Цена'] > 120]
    df_res = df_res1.loc[df_res1['Производитель'] != df_res1['Модель']]
    df_res['Производитель'] = df_res['Производитель'].str.lower()
    df_res['Производитель'] = df_res['Производитель'].str.replace(' ', '')
    return df_res

models_list = []


def split_continental():
    models_new_list = []
    df_res = create_first_df()
    for i in range(0, len(df_res)):
        model = df_res.iloc[i]['Модель'].lower().replace(' ', '').replace('-', '')
        models_new_list.append(model)
    if len(models_new_list) == len(df_res):
       try:
          df_res['update_models'] = models_new_list
       except Exception:
          print('[Error]')
    else:
        print('something gonna wrong')
    return df_res

def function_lower(x):
    return x.str.lower()

def groupby_summ_and_seria_to_column():
    dff = split_continental()
    dff[['Производитель', 'Модель']].apply(function_lower)
    df = dff.loc[dff['Производитель'] != dff['Модель']]
    df_mean_price = df.groupby('update_models')['Цена'].mean()
    indexes = [i for i in range(0, len(df))]
    df_good = pd.DataFrame(df.values, index=indexes, columns=df.columns)
    for i in range(0, len(df_good)):
        model = df_good.iloc[i]['update_models']
        for j in range(0, len(df_mean_price)):
            if model == df_mean_price.index.values[j]:
                df_good.at[i, 'Средняя цена'] = df_mean_price[j]
                df_good.at[i, 'Отклонение от средней'] = df_good.iloc[i]['Цена'] - df_good.iloc[i]['Средняя цена']
                i += 1
    return df_good

def delete_extra(df):

    df_short = df.loc[df['Производитель'] != df['Модель']]
    #with pd.ExcelWriter('factoring/data.xlsx') as writer:
        #df_short.to_excel(writer, sheet_name='Sheet_name_1')
    return df_short




df = delete_extra(groupby_summ_and_seria_to_column())

def groupby_count():
    seria = df.groupby('update_models')['update_models'].count()
    with pd.ExcelWriter('statistic/models_count.xlsx') as writer:
        seria.to_excel(writer, sheet_name='numeric')
    return seria


def groupby_count_production():
    seria = df.groupby('Производитель')['Производитель'].count()
    seria = seria[seria > 5]
    print(type(seria))
    return seria



def seria_to_column(df, seria):
    for i in range(0, len(df)):
        model = df.iloc[i]['update_models']
        for j in range(0, len(seria)):
            if model == seria.index.values[j]:
                df.at[i, 'Число предложений'] = seria[j]
                i += 1
    return df


def to_exel(df):
    with pd.ExcelWriter('dataframe/main_files/full_data.xlsx') as writer:
        df.to_excel(writer, sheet_name='full_data')


df_res = seria_to_column(df, groupby_count())



def define_classes(df):
    df1 = df.groupby('Производитель')['Цена'].mean()
    df2 = df.groupby('Производитель')['Производитель'].count()
    df3 = pd.DataFrame(df1)
    df3['Всего предложений производителя'] = df2
    for i in range(0, len(df)):
        production = df.iloc[i]['Производитель']
        for j in range(0, len(df1)):
            if production == df1.index.values[j]:
                df.at[i, 'Средняя цена производителя'] = df1[j]
                i += 1
    return df3


def define_quality(df):
    df['Коэфициент износа'] = 4
    for j in range(0, len(df)):
        left = [int(i) for i in str(df.iloc[j]['Остаток протектора']).replace('[', '').replace(']', '').replace(',', '').replace(' ', '').replace('n', '').replace('a', '')]
        if len(left) > 0:
            if len([i for i in left if int(i) > 6 and i < 9]) > 0:
               df.at[j, 'Коэфициент износа'] = 1
            elif len([int(i) for i in left if int(i) == 6]) > 0:
               df.at[j, 'Коэфициент износа'] = 2
            elif len([int(i) for i in left if int(i) > 3 and i < 6]) > 0:
               df.at[j, 'Коэфициент износа'] = 3
        elif df.iloc[j]['Год'] != 'no year' and df.iloc[j]['Год'] != None:

            year = float(df.iloc[j]['Год'])
            max = [2019, 2020]
            mid = [2016, 2017, 2018]
            min = [2013, 2014, 2015]
            if year in max:
                df.at[j, 'Коэфициент износа'] = 1
            elif year in mid:
                df.at[j, 'Коэфициент износа'] = 2
            elif year in min:
                df.at[j, 'Коэфициент износа'] = 3
        else:
            comment = str(df.iloc[j]['Описание']).split(' ')
            good_words = ['идеальном', 'отличное', 'новые', 'идеальное']
            if any(i in good_words for i in comment):
                df.at[j, 'Коэфициент износа'] = 3
            else:
                df.at[j, 'Коэфициент износа'] = 4
    return df





def main():
    to_exel(define_quality(df_res))
    #to_exel(production_mean_price())
    #df33 = groupby_count_production()
    #with pd.ExcelWriter('statistic/prod_by_count.xlsx') as writer:
        #df33.to_excel(writer, sheet_name='full_data')
    #groupby_count()
    #groupby_mean()












