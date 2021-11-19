import re


str = 'BF Goodrich G-Grip 195/65R15 95T, с пробегом, 4 шт.'
print(re.split('2|1', str)[0])