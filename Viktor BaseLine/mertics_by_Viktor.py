# $$
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import plotly.graph_objs as go
import missingno as msn
from fancyimpute import KNN
import warnings

warnings.filterwarnings("ignore")

# %%
train_data = pd.read_csv("../merged_data_without_links.csv")

# Предобработка данных
def preprocess_data(df):
    df = df.drop(columns='report_date', errors='ignore')
    df = df.loc[:, df.isnull().mean() < 0.8]
    df_target_0 = df[df['target'] == 0]
    df_target_1 = df[df['target'] == 1]
    return df_target_0, df_target_1
# %%
train_data["report_date"] = pd.to_datetime(train_data["report_date"], format="%Y-%m-%d")
train_data = train_data.select_dtypes(exclude=["object"])
train_data = train_data.fillna(0)
df_target_0, df_target_1 = preprocess_data(train_data)

# %% 
msn.bar(df_target_1, fontsize=10, color=(1, 0.75, 0.8))

# %%
df_filled_0 = pd.DataFrame(KNN(k=9).fit_transform(df_target_0), columns=df_target_0.columns)
df_filled_1 = pd.DataFrame(KNN(k=9).fit_transform(df_target_1), columns=df_target_1.columns)
df_combined = pd.concat([df_filled_0, df_filled_1])

# %%
X = df_combined.drop(columns='target')
y = df_combined['target']

scaler = StandardScaler()
X = scaler.fit_transform(X)

smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# %%
rf_model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)

auc = metrics.roc_auc_score(y_test, y_pred_proba)
print(f"AUC: {auc:.3f}")

# %%
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()

# %% 
# Интерактивная ROC-кривая
trace = go.Scatter(x=fpr, y=tpr, mode='lines', name=f'AUC = {auc:.2f}',
                   line=dict(color='darkorange', width=2))
reference_line = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Reference Line',
                            line=dict(color='navy', width=2, dash='dash'))
fig = go.Figure(data=[trace, reference_line])
fig.update_layout(title='Interactive ROC Curve',
                  xaxis_title='False Positive Rate',
                  yaxis_title='True Positive Rate')
fig.show()