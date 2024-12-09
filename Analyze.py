# %% Импорт библиотек, чтение и вывод (первые 10 строк) данных
import pandas as pd
import numpy as np

df = pd.read_csv('train.csv')

df.head(10)

# %% Удаление пустых колонок и вывод первых 10 строк для наблюдения, что изменилось
df.dropna(how='all', axis=1, inplace=True)

df.head(10)
# %%
