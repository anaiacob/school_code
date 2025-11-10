import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from scipy.stats import chi2_contingency

# === SETUP
sns.set(style="whitegrid")
os.makedirs("output", exist_ok=True)

# === Incarcare date
df = pd.read_csv("heart_4_train.csv")

# === Atribute
continuous = [
    'age', 'systolic_pressure', 'diastolic_pressure', 'cholesterol_level',
    'heart_rate', 'mass_index', 'blood_sugar_level', 'sleep_heart_rate', 'ldl_cholesterol'
]
discrete = ['daily_cigarettes']
categorical = [
    'blood_pressure_medication', 'smoking_status', 'hypertension_history',
    'stroke_history', 'diabetes_history', 'high_blood_sugar',
    'gender', 'education_level'
]
target = 'chd_risk'

# === 1. Boxplot continuu
plt.figure(figsize=(16, 10))
sns.boxplot(data=df[continuous], orient="h")
plt.title("Boxplot - Atribute Numerice Continue")
plt.tight_layout()
plt.savefig("output/boxplot_continuous.png")
plt.close()

# === 2. Histograme pentru categorice si discrete
for col in discrete + categorical:
    plt.figure()
    df[col].dropna().value_counts().sort_index().plot(kind="bar")
    plt.title(f"Distributie {col}")
    plt.xlabel(col)
    plt.ylabel("Frecventa")
    plt.tight_layout()
    plt.savefig(f"output/hist_{col}.png")
    plt.close()

# === 3. Distributia claselor
plt.figure()
df[target].value_counts().sort_index().plot(kind="bar")
plt.title("Distributia etichetei tinta (chd_risk)")
plt.xticks(rotation=0)
plt.savefig("output/class_distribution.png")
plt.close()

# === 4. Corelatii Pearson (numerice)
plt.figure(figsize=(12, 10))
sns.heatmap(df[continuous].corr(), annot=True, cmap='coolwarm', square=True)
plt.title("Corelatie intre Atributele Numerice")
plt.tight_layout()
plt.savefig("output/heatmap_numeric.png")
plt.close()

# === 5. Corelatii categorice (Cramer's V)
def cramers_v(x, y):
    table = pd.crosstab(x, y)
    chi2, _, _, _ = chi2_contingency(table)
    n = table.sum().sum()
    return np.sqrt(chi2 / (n * (min(table.shape) - 1)))

cat_matrix = pd.DataFrame(index=categorical, columns=categorical)
for i in categorical:
    for j in categorical:
        if i == j:
            cat_matrix.loc[i, j] = 1.0
        else:
            cat_matrix.loc[i, j] = cramers_v(df[i], df[j])

plt.figure(figsize=(10, 8))
sns.heatmap(cat_matrix.astype(float), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Corelatie intre Atribute Categoriale")
plt.tight_layout()
plt.savefig("output/heatmap_categorical.png")
plt.close()

# === 6. Preprocesare
X = df.drop(columns=[target])
y = df[target]

X = pd.DataFrame(SimpleImputer(strategy="mean").fit_transform(X), columns=X.columns)
X = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)

# === 7. impartire date
for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42 + i)
    if len(np.unique(y_test)) == 2:
        break
else:
    raise ValueError("Nu s-au gasit ambele clase in y_test")

# === 8. Clasificatori + evaluare
models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, class_weight="balanced", random_state=0),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=7, class_weight="balanced", random_state=0),
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "MLP Classifier": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=0)
}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
