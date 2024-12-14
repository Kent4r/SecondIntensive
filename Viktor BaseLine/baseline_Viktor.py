# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import plotly.graph_objs as go

# %%
train_data = pd.read_csv("../merged_data_without_links.csv")
valid_data = pd.read_csv("../valid/processed_valid.csv")

valid_data["report_date"] = pd.to_datetime(valid_data["report_date"], format="%Y-%m-%d")
valid_data = valid_data.select_dtypes(exclude=["object"])
valid_data = valid_data.fillna(0)

# %%
X_valid = valid_data.drop(
    ["target", "report_date"], axis=1
)  # Удаляем целевую переменную и report_date
y_valid = valid_data["target"]  # Берем только целевую переменную
X_train, X_test, y_train, y_test = train_test_split(
    X_valid, y_valid, test_size=0.3, random_state=0
)

# %%
log_regression = LogisticRegression()
log_regression.fit(X_train, y_train)

# предсказание вероятностей
y_pred_proba = log_regression.predict_proba(X_test)[:, 1]
fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)

auc = metrics.roc_auc_score(y_test, y_pred_proba)
print(f"AUC: {auc:.3f}")

# %%
trace = go.Scatter(y=fpr, x=tpr, mode='lines', name=f'AUC = {auc:.2f}',
                   line=dict(color='darkorange', width=2))
reference_line = go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Reference Line',
                            line=dict(color='navy', width=2, dash='dash'))
fig = go.Figure(data=[trace, reference_line])
fig.update_layout(title='Interactive ROC Curve',
                  xaxis_title='False Positive Rate',
                  yaxis_title='True Positive Rate')
fig.show()

# %%
