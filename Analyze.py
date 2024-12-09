# %% Импорт библиотек, чтение и вывод фигуры данных
import pandas as pd
import numpy as np

df = pd.read_csv('train.csv')
df.shape

# %% Удаление пустых колонок и смотрим, что изменилось
df.dropna(how='all', axis=1, inplace=True)
df.shape
# %% смотрим сколько колонок какого типа
df.info()
# %% записываем весь список колонок типа obj
f = open('list_of_object_col.txt', 'w')
f.write(f"{str(list(df.select_dtypes(['object']).columns)).replace(', ', '\n').replace("'", '').replace('[','').replace(']', '')}")
f.close()
# %%
