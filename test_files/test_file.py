import re
import json

s = 'Отличная зимняя резина, остаток 6-7 мм, цена за 1 колесо, комплектом д120ешевле'
with open('../av/av_by_parser.json', encoding='utf-8') as file:
    data = json.load(file)
i = 0
for item in data:
    comment = item.get('Описание')
    print(comment)
    commnt = str(comment).replace('4 шт', ' ').replace('4 колеса', ' ').replace('5x', '').replace('6x', '')
    nums = re.findall(r'\d*\.\d+|\d+', commnt)
    numss = list(filter(lambda i: float(i) in range(3, 10), nums))
    if len(numss) > 0:
        print(numss)
    else:
        i += 1
        print(f'[NOT FOUND] {i} ')

