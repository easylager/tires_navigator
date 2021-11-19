import pandas as pd
from sockets import upgrade


seria = pd.read_excel(io='../dataframe/statistic/prod_by_count.xlsx', engine='openpyxl')
models_list = list((seria['Производитель']))
df = pd.read_excel(io='../dataframe/main_files/full_data.xlsx', engine='openpyxl')
for j in models_list:
    for i in range(1, len(df)):
        if df.iloc[i]['Производитель'] == j:
           print(f'{j} ----  {df[i]}')