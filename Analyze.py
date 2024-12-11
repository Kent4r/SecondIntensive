# %%
# Импорт библиотек, чтение и вывод фигуры данных
import pandas as pd
import numpy as np

df = pd.read_csv('train.csv')
df.shape

# %%
# Удаление пустых колонок, дропаем дупликаты и смотрим, что изменилось
df = df.replace([np.inf, -np.inf, np.nan], 0)
df.dropna(how='all', axis=1, inplace=True)
df.drop_duplicates()
df.shape

# %%
# Удаляем все колонки, у которых наполненность менее 0.1%
df = df.loc[:, ((df == 0) | (df.isnull())).mean() < 0.999]
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
# Переводим колонки Float64 в Int64, которые можем
float_columns = df.select_dtypes(include=np.number).columns
for col in float_columns:
    temp = df[col].fillna(0)
    if temp.apply(lambda x: x == int(x)).all():
        df[col] = df[col].astype(int)
# %%
# Делаем то же самое, но с float64
text = ""
for col in list(df.select_dtypes(['float']).columns): text += f"{col}:\n{df[col].unique()}\n\n\n"
f = open('list_of_unique_values_in_float_cols.txt', 'w', encoding='utf-8')

# dic = {'nan':'',"' ":'\n'," '":'',"'":'','[':'',']':'','  ':'',}
# for i, j in dic.items(): text = text.replace(i, j)

f.write(text)
f.close()
# %%

# %%
df.to_csv("cleaned_data.csv", index=False)
# %%
df.info()
# %%
