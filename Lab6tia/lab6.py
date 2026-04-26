import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
# Citirea setului de date
file_name = 'smokers_v2.csv'
df = None

try:
    df = pd.read_csv(file_name)
    print(f"Citirea fisierului Excel '{file_name}' a fost realizata cu succes!")
except FileNotFoundError:
    print(f"Eroare: Fisierul '{file_name}' nu a fost gasit. Asigurati-va ca este în aceeasi locatie cu scriptul.")
    exit()
except ImportError:
    print(f"Eroare: Va rugam sa instalati biblioteca openpyxl.")
    exit()
except Exception as e:
    print(f"A aparut o eroare la citirea fisierului: {e}")
    exit()

if df.columns[0] == "Unnamed: 0":
    df.rename(columns={"Unnamed: 0": "index"}, inplace=True)

# Verificare structurii setului de date
print("Verificare structura initiala")
print(df.head())
print(df.info())
print("\n")

print("Valori lipsa pe coloana:")
print(df.isnull().sum())

# Eliminarea randurilor cu valori lipsa
df = df.dropna()

# Eliminarea indexului
df = df.drop(columns=["index"])

# Verificare si eliminare duplicatele din dataset
initial_rows = len(df)
duplicate_count = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"Eliminarea duplicatelor")
print(f"Numar de randuri initiale: {initial_rows}")
print(f"Numar de duplicate gasite si eliminate: {duplicate_count}")
print(f"Numar de randuri dupa eliminarea duplicatelor: {len(df)}")
print("\n")

print("Distributia clasei target:")
print(df["smoking"].value_counts())
print('\n')

# Pentru Random Forest, care nu accepta alte valori decat numerice
label_encoders = {}

for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

numeric_cols = df.select_dtypes(include=np.number).columns

# Detectare valori extreme
outliers = {}
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    outliers[col] = ((df[col] < q1 - 1.5 * iqr) | 
                     (df[col] > q3 + 1.5 * iqr)).sum()

print("Numar de outlieri per coloana:")
print(outliers)

print('\n')
print('\n')

#Histograme pt principalele coloane
plt.figure()
df["smoking"].hist()
plt.title("Distributia variabilei tinta (smoking)")
plt.xlabel("Smoker (0 = Nu, 1 = Da)")
plt.ylabel("Frecventa")
plt.show()

plt.figure()
df[df["smoking"] == 0]["fasting blood sugar"].hist(alpha=0.7, bins=20, label="Non-smoker")
df[df["smoking"] == 1]["fasting blood sugar"].hist(alpha=0.7, bins=20, label="Smoker")
plt.title("Distributia fasting blood sugar pe clase")
plt.xlabel("fasting blood sugar")
plt.ylabel("Frecventa")
plt.legend()
plt.show()
# Cerinta 2
X = df.drop("smoking", axis=1)
y = df["smoking"]

print("Dimensiunea setului X:", X.shape)
print("Dimensiunea setului y:", y.shape)
print('\n')
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

rf_configs = [
    {
        "n_estimators": 100,
        "max_depth": 5,
        "min_samples_split": 2,
        "random_state": 42
    },
    {
        "n_estimators": 200,
        "max_depth": 10,
        "min_samples_split": 5,
        "random_state": 42
    },
    {
        "n_estimators": 300,
        "max_depth": 15,
        "min_samples_split": 10,
        "random_state": 42
    }
]

results = []

for i, config in enumerate(rf_configs, start=1):
    print(f"\n           Model {i}           ")
    # Initializarea modelului Random Forest
    rf = RandomForestClassifier(**config)
    # Antrenarea modelului
    rf.fit(X_train, y_train)
    # Predictii pe setul de test
    y_pred = rf.predict(X_test)
    # Calcularea metricilor
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    # Salvarea rezultatelor
    results.append({
        "Model": i,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })
    # Afisarea rezultatelor
    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1)
    print("Matricea de confuzie:\n", cm)
    
    #Plotare matrice de confuzie
    plt.figure()
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues")
    disp.plot()
    plt.title(f"Matricea de confuzie - Model {i}")
    plt.show()

# Compararea modelelor și alegerea celui mai bun
results_df = pd.DataFrame(results)

print("\n           REZULTATE FINALE            ")
print(results_df)

best_model = results_df.loc[results_df["F1 Score"].idxmax()]

print("\n           CEL MAI BUN MODEL (după F1)            ")
print(best_model)