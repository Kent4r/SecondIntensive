# %%
import pandas as pd
import numpy as np
import re

# Загружаем CSV-файл
df = pd.read_csv("csv_int64.csv", dtype=np.float64)  # Сначала загружаем как float64

df = df.drop(["client_id","target"],axis=1)
df.replace("nan",np.nan, inplace=True)


def merge_columns_with_common_values(df):
    base_toggle = True
    count = 0
    unique_columns = []
    temp_col = "col2"

    # Преобразуем DataFrame в строки для сравнения
    # df.astype(str)

    # Создаем словарь для группировки колонок с общими значениями
    column_groups = {}

    for col in df.columns:
        if col in unique_columns:
            continue

        if col != df.columns[1]: base_toggle = False

        # Инициализируем группу для текущей колонки
        column_groups[col] = [col]

        for next_col in df.columns:
            if col == next_col or next_col in unique_columns:
                continue

            # Находим общие уникальные значения между текущей и следующей колонкой
            common_values = list(set(df[col].unique()).intersection(set(df[next_col].unique())))
            if np.nan in common_values:
                common_values.remove(np.nan)  # Убираем -1, если он есть

            # count jump by col number
            match = re.match(r"([a-zA-Z]+)(\d{1,4})", col)
            match1 = re.match(r"([a-zA-Z]+)(\d{1,4})", next_col)
            def calc_jump():
                if base_toggle:return False
                else:
                    match = re.match(r"([a-zA-Z]+)(\d{1,4})", temp_col)
                    is_jump = (int(match1.group(2)) - int(match.group(2))) > 5
                    return is_jump

            # Упрощенные критерии объединения
            if (len(common_values) >= 1):  # Объединяем, если есть хотя бы одно общее значение
                if calc_jump():
                    temp_col = next_col
                    break
                count += 1
                temp_col = next_col
                column_groups[col].append(next_col)  # Добавляем колонку в группу
                unique_columns.append(next_col)  # Помечаем колонку как обработанную
                print(f"Merged {col} and {next_col}: common_values = {common_values}")
            else:
                if calc_jump():
                    temp_col = next_col
                    break
                common_values = list(
                    set(df[temp_col].unique()).intersection(set(df[next_col].unique()))
                )
                if len(common_values) >= 1:
                    count += 1
                    temp_col = next_col
                    column_groups[col].append(next_col)  # Добавляем колонку в группу
                    unique_columns.append(next_col)  # Помечаем колонку как обработанную
                    print(f"Merged {col} and {next_col}: common_values = {common_values}")
                else:break

        # Помечаем текущую колонку как обработанную
        unique_columns.append(col)

    # Объединяем колонки в каждой группе
    for group_name, group_columns in column_groups.items():
        if len(group_columns) > 1:  # Если в группе больше одной колонки
            df[group_name] = (df[group_columns].bfill(axis=1).iloc[:, 0])  # Объединяем колонки
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

# Заменяем все -1 на NaN
df_merged.replace(-1, np.nan, inplace=True)

# Сохраняем результат в новый CSV-файл
df_merged.to_csv("merged_int64.csv", index=False)

# Проверяем результат
clean_int = pd.read_csv("merged_int64.csv")
print(clean_int.shape)
# %%
