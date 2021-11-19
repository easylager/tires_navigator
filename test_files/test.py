import pandas as pd
import json

with open('../av/av_by_parser_test.json', 'r', encoding='utf-8') as file:
    dict = json.load(file)
df = pd.DataFrame.from_dict(dict)
print(df)