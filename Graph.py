#%%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as ss
import missingno as msn

df = ss.read_csv('merged_data_without_links.csv')

msn.bar(df, fontsize=10, color=(1, 0.75, 0.8))
# %%
# df = df.loc[:, ((df == 0) | (df.isnull())).mean() < 0.70]
msn.bar(df, fontsize=10, color=(1, 0.75, 0.8))
# %%
df.info()
# %%
text = ""
for col in list(df.columns): text += f"{col}:\n{str(df[col].unique())}\n\n\n"
f = open('txt/unique_vals_in_merged_data_without_links.txt', 'w', encoding='utf-8')

dic = {'nan':'',    "' ":'\n',  " '":'',    "'":'',     '[':'',     ']':''}
for i, j in dic.items(): text = text.replace(i, j)

f.write(text)
f.close()

# %%
# TODO: ДРОПАТЬ НАХУЙ КОЛОННЫ С ССЫЛКАМИ
def has_link(column):
    return column.astype(str).str.startswith(('http://', 'https://'), na=False).any()

# Удаление столбцов, содержащих ссылки
df = df.loc[:, ~df.apply(has_link)]

has_link(df.columns)

df.to_csv('merged_data_without_links.csv', index=False)

# %%
import pandas as pd

df = pd.read_csv('merged_data_without_links.csv')

# df['report_date'] = pd.to_datetime(df['report_date'], format='%Y-%m-%d')
# df = df.select_dtypes(exclude=['object'])
df.info()
# %%
df.to_csv('merged_data_without_links.csv', index=False)

# %%
