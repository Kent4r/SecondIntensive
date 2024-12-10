# %%
# Импорт библиотек, чтение и вывод фигуры данных
import pandas as pd
import numpy as np

df = pd.read_csv('train.csv')
df.shape

# %%
# Удаление пустых колонок и смотрим, что изменилось
df.dropna(how='all', axis=1, inplace=True)
df.shape
# %%
# смотрим сколько колонок какого типа
df.info()
# %%
# записываем весь список колонок типа obj
f = open('list_of_object_cols.txt', 'w')
f.write(f"{str(list(df.select_dtypes(['object']).columns)).replace(', ', '\n').replace("'", '').replace('[','').replace(']', '')}")
f.close()
# %%
# Смотрим все уникальные значения колонок obj
text = ""
for col in list(df.select_dtypes(['object']).columns): text += f"{col}:\n{str(df[col].unique())}\n\n\n"
f = open('list_of_unique_values_in_object_cols.txt', 'w', encoding='utf-8')

dic = {'nan':'',    "' ":'\n',  " '":'',    "'":'',     '[':'',     ']':''}
for i, j in dic.items(): text = text.replace(i, j)

f.write(text)
f.close()
# %%
# Делаем то же самое, но с float64
text = ""
for col in list(df.select_dtypes(['float']).columns): text += f"{col}:\n{str(df[col].unique())}\n\n\n"
f = open('list_of_unique_values_in_float_cols.txt', 'w', encoding='utf-8')

dic = {'nan':'',"' ":'\n'," '":'',"'":'','[':'',']':'','  ':'',}
for i, j in dic.items(): text = text.replace(i, j)

f.write(text)
f.close()
# %%
