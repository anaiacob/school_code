import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE

FILE_NAME = "smokers.csv"

df = pd.read_csv(FILE_NAME, index_col=0)
#CERINTA 1
print("Valori lipsa pe coloana:\n")
print(df.isna().sum())

# cont_cols = [
#     col for col in df.columns
#     if df[col].isna().sum()==0
# ]
# plt.figure(figsize=(16,10))
# for i, col in enumerate(cont_cols,1):
#     plt.subplot(3,4,i)
#     plt.hist(df[col].dropna(), bins=50)
#     lower = df[col].min() - (df[col].std() * 1)
#     upper = df[col].max() + (df[col].std() * 1)
#     plt.xlim(lower, upper)

#     plt.title(col)
# plt.tight_layout()
# plt.show()
# plt.savefig("Histograma.png")

df.hist(figsize=(15, 10), bins=50)
plt.suptitle("Distribuția Variabilelor Numerice", y=1.02)
plt.show()
#CERINTA 2
df = df.fillna(df.median(numeric_only=True))
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matricea de corelatie")
plt.show()
df = df.drop(columns=["education", "currentSmoker"], errors="ignore")

scaler = StandardScaler()

#CERINTA 3
df["TenYearCHD"].value_counts().plot(kind="bar")
plt.title("Distribuția țintei TenYearCHD")
plt.show()
X = df.drop(columns=["TenYearCHD"])
y = df["TenYearCHD"]
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
log_reg = LogisticRegression(max_iter=500)
svc = SVC(kernel= "poly", degree=4, C=0.01, class_weight="balanced", gamma=0.2)

log_reg.fit(X_train, y_train)
svc.fit(X_train, y_train)

def evaluate(model, name):
    y_pred = model.predict(X_test)
    print(f"\n===== {name} =====")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
    plt.title(f"Matrice de confuzie - {name}")
    plt.show()

evaluate(log_reg, "Logistic Regression")
evaluate(svc, "SVC")

#CERINTA 5
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

log_reg_sm = LogisticRegression(max_iter=500)
svc_sm = SVC(kernel='rbf', probability=True)

log_reg_sm.fit(X_train_sm, y_train_sm)
svc_sm.fit(X_train_sm, y_train_sm)

evaluate(log_reg_sm, "Logistic Regression Smote")
evaluate(svc_sm, "SVC Smote")
