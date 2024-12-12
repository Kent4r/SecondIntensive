# %%
import pandas as pd
import numpy as np

# Загружаем CSV-файл
df = pd.read_csv("csv_float64.csv", dtype=np.float64)


def merge_columns_with_common_values(df):
    count = 0
    unique_columns = []
    
    # Преобразуем DataFrame в строки для сравнения
    df_str = df.astype(str)
    df.replace("nan", np.nan, inplace=True)  # Убираем только "nan"
    
    # Создаем словарь для группировки колонок с общими значениями
    column_groups = {}
    
    for col in df.columns:
        if col in unique_columns:
            continue
        
        # Инициализируем группу для текущей колонки
        column_groups[col] = [col]
        
        for next_col in df.columns:
            if col == next_col or next_col in unique_columns:
                continue
            
            # Находим общие уникальные значения между текущей и следующей колонкой
            common_values = list(set(df[col].unique()).intersection(set(df[next_col].unique())))
            if np.nan in common_values:
                common_values.remove(np.nan)
            
            # Упрощенные критерии объединения
            if len(common_values) >= 1:  # Объединяем, если есть хотя бы одно общее значение
                count += 1
                column_groups[col].append(next_col)  # Добавляем колонку в группу
                unique_columns.append(next_col)  # Помечаем колонку как обработанную
                print(f"Merged {col} and {next_col}: common_values = {common_values}")
        
        # Помечаем текущую колонку как обработанную
        unique_columns.append(col)
    
    # Объединяем колонки в каждой группе
    for group_name, group_columns in column_groups.items():
        if len(group_columns) > 1:  # Если в группе больше одной колонки
            df[group_name] = df[group_columns].bfill(axis=1).iloc[:, 0]  # Объединяем колонки
            print(f"Merged columns {group_columns} into {group_name}")
        else:
            df[group_name] = df[group_columns[0]]  # Оставляем колонку как есть
    
    # Удаляем исходные колонки, которые были объединены
    df = df[[col for col in df.columns if col in column_groups]]
    
    return df, count

df_merged, count = merge_columns_with_common_values(df)

if count == 0:
    print("Nothing changed!")
else:
    print(f"{count} columns were merged.")

# Сохраняем результат в новый CSV-файл
df_merged.to_csv('merged_float.csv', index=False)
# %%
df_mer = pd.read_csv("merged_float.csv")
df_mer.shape
# %%
