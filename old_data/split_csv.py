#%%
import pandas as pd
import numpy as np
import re

df_int = pd.read_csv("merged_csv/merged_int64.csv")
df_float = pd.read_csv("merged_csv/merged_float.csv", dtype=np.float64)
df_object = pd.read_csv("merged_csv/merged_object.csv")
df_id_target = pd.read_csv("train.csv")

df_not_sorted = pd.concat([df_object['report_date'],df_id_target['client_id'], df_id_target['target']],axis=1)
df_object.drop(columns='report_date', inplace=True)

df_not_sorted = pd.concat([df_not_sorted, df_object, df_int, df_float],axis=1)
df_not_sorted.info()

# %%
order_dict = {}
order_list = ['report_date','client_id','target']
columns = df_not_sorted.columns
for column in columns:
    if 'col' in column:
        order_dict[column] = int(re.match(r"([a-zA-Z]+)(\d{1,4})", column).group(2))

# sorted(order_list.items(), key=lambda x: x[1])
sorted_columns = {k: v for k, v in sorted(order_dict.items(), key=lambda item: item[1])}
for k in sorted_columns:
    order_list.append(k)

df_sorted = df_not_sorted[order_list]

# %%
df_not_sorted.to_csv("merged_data.csv",index=False)
# %%
