import pandas as pd
from pandas import read_csv
import json

def upgrade():
    df = pd.read_excel(io='../dataframe/main_files/full_data.xlsx', engine='openpyxl')

    seria = df.groupby('Размер')['Цена'].mean()
    for i in range(1, len(df)):
        size = df.iloc[i]['Размер']
        for j in range(1, len(seria)):
            if seria.index.values[j] == size:
                df.at[i, 'avg_size_price'] = seria[j]
                df.at[i, 'split_size_price'] = df.iloc[i]['Цена'] - df.iloc[i]['avg_size_price']
                i += 1
    dfres = df[df['Отклонение от средней'] < 0]
    df_res = dfres[dfres['split_size_price'] < 0]
    #указываем нужные размеры
    size_list = ["{'Ширина': 215.0, 'Высота': 60.0, 'Диаметр': 16.0}", "{'Ширина': 215.0, 'Высота': 65.0, 'Диаметр': 15.0}"]
    short_list = []
    for i in range(1, len(df_res)):
        size = (df_res.iloc[i]['Размер'])
        if size in size_list:
            short_list.append(dict(df.iloc[i]))
    dfs = pd.DataFrame(short_list)
    print(dfs)
    results = dfs.to_json(orient='index')
    parsed = json.loads(results)

    with open('215_60-65-16.json', 'w', encoding='utf-8') as file:
        json.dump(parsed, file, indent=4, ensure_ascii=False)

upgrade()