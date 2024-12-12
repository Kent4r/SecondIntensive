# %%
import pandas as pd
import numpy as np

# Загружаем CSV-файл
df = pd.read_csv('csv_float64.csv')

# Преобразуем все столбцы в тип object (если они уже не object)
df = df.astype(str)
df.replace('0.0', np.nan, inplace=True)
df.replace('1.0', np.nan, inplace=True)
df.replace('nan', np.nan, inplace=True)

# Функция для объединения столбцов, если они имеют общие уникальные значения
def merge_columns_with_common_values(df):
    global count
    count = 0
    columns = df.columns.tolist()
    merged_columns = []
    i = 0
    while i < len(columns) - 1:
        current_col = columns[i]
        next_col = columns[i + 1]
        
        # Находим общие уникальные значения между текущим и следующим столбцом
        common_values = list(set(df[current_col].unique()).intersection(set(df[next_col].unique())))
        x = np.nan
        if(x in common_values): common_values.remove(x)
        # print(common_values)
        # if len(common_values) > 1 or (len(common_values) == 1 and len(df[current_col].unique()) < 3):

        if len(common_values) >= 10:
            A = len(df[current_col].unique())/5 < len(common_values)
        else:
            A = len(df[current_col].unique())/3 < len(common_values)
        
        if A:
            if current_col == "col47": print(common_values)
            # Объединяем столбцы, если есть общие значения
            count += 1
            merged_name = f"{current_col}"
            df[merged_name] = df[current_col].combine_first(df[next_col])
            merged_columns.append(merged_name)
            i += 2  # Пропускаем следующий столбец, так как он уже объединен
        else:
            merged_columns.append(current_col)
            i += 1
    
    # Если остался последний столбец, который не был объединен
    if i == len(columns) - 1:
        merged_columns.append(columns[-1])
    
    # Оставляем только объединенные столбцы
    df = df[merged_columns]
    return df

# Применяем функцию
df_merged = merge_columns_with_common_values(df)
i = 1
while count != 0:
    i += 1
    df_merged = merge_columns_with_common_values(df_merged)
    print(f"Iteration {i}: {len(df_merged.columns)} columns left")


if count == 0:
    print("Nothing changed!")

# Сохраняем результат в новый CSV-файл
df_merged.to_csv('merged_float.csv', index=False)
# %%
