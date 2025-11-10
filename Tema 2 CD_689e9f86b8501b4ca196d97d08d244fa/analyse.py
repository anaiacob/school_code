# Exploratory Data Analysis pentru Tema 2 - Cerinta 3.1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from collections import Counter

# Citirea datelor
heart_path = "heart_4_train.csv"
pirvision_path = "pirvision_office_train.csv"

heart_train = pd.read_csv(heart_path)
pirvision_train = pd.read_csv(pirvision_path)

# --------------------
# Explorare: Heart Dataset
# --------------------

# 1. Atribute numerice
heart_numeric = heart_train.select_dtypes(include=[np.number]).drop(columns=["chd_risk"])
heart_numeric_stats = heart_numeric.describe(percentiles=[.25, .5, .75]).T
heart_numeric_stats['non_null_count'] = heart_numeric.count()
heart_numeric_stats = heart_numeric_stats[[
    'non_null_count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]

# Salvare statistici numerice
heart_numeric_stats.to_csv("heart_numeric_stats.csv")

# Boxplot pentru atribute numerice
plt.figure(figsize=(15, 10))
heart_numeric.boxplot(rot=90)
plt.title("Boxplot - Atribute numerice (Heart Dataset)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("heart_boxplot.png")
plt.close()

# 2. Atribute categorice
heart_categorical_cols = ['gender', 'education_level', 'smoking_status',
                          'hypertension_history', 'stroke_history', 'diabetes_history',
                          'blood_pressure_medication', 'high_blood_sugar']

cat_summary = []
for col in heart_categorical_cols:
    non_null = heart_train[col].notnull().sum()
    unique_vals = heart_train[col].nunique()
    cat_summary.append((col, non_null, unique_vals))

heart_categorical_summary = pd.DataFrame(cat_summary, columns=['Atribut', 'Nr. non-null', 'Valori unice'])
heart_categorical_summary.to_csv("heart_categorical_summary.csv", index=False)

# Histograme
for col in heart_categorical_cols:
    plt.figure(figsize=(5, 3))
    sns.countplot(x=heart_train[col])
    plt.title(f"Distributie - {col}")
    plt.tight_layout()
    plt.savefig(f"heart_hist_{col}.png")
    plt.close()

# 3. Eticheta tinta
plt.figure(figsize=(5, 3))
sns.countplot(x=heart_train["chd_risk"])
plt.title("Distributie eticheta tinta - chd_risk")
plt.tight_layout()
plt.savefig("heart_chd_risk_dist.png")
plt.close()

# 4. Corelatii Pearson
corr_matrix = heart_numeric.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', square=True, linewidths=0.5)
plt.title("Matricea de corelatie Pearson - Heart")
plt.tight_layout()
plt.savefig("heart_corr_heatmap.png")
plt.close()

# --------------------
# Explorare: PIRvision Dataset
# --------------------

pirvision_numeric = pirvision_train.select_dtypes(include=[np.number]).drop(columns=["Class"])
pirvision_numeric_stats = pirvision_numeric.describe(percentiles=[.25, .5, .75]).T
pirvision_numeric_stats['non_null_count'] = pirvision_numeric.count()
pirvision_numeric_stats = pirvision_numeric_stats[[
    'non_null_count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]
pirvision_numeric_stats.to_csv("pirvision_numeric_stats.csv")

# Boxplot pentru primele OBS-uri
sample_obs_cols = [f'OBS_{i}' for i in range(1, 10)] + ['Temp (C)']
plt.figure(figsize=(15, 8))
pirvision_train[sample_obs_cols].boxplot(rot=90)
plt.title("Boxplot - OBS selectate (PIRvision)")
plt.tight_layout()
plt.savefig("pirvision_boxplot.png")
plt.close()

# Distributia claselor
plt.figure(figsize=(5, 3))
sns.countplot(x=pirvision_train["Class"])
plt.title("Distributie eticheta titnta - Class (PIRvision)")
plt.tight_layout()
plt.savefig("pirvision_class_dist.png")
plt.close()

# Corelatii OBS (primele 20 pentru lizibilitate)
obs_cols = [col for col in pirvision_numeric.columns if col.startswith("OBS_")]
subset_cols = obs_cols[:20]
plt.figure(figsize=(14, 10))
sns.heatmap(pirvision_train[subset_cols].corr(), annot=False, cmap='coolwarm', square=True)
plt.title("Corelatie Pearson - Primele 20 OBS-uri")
plt.tight_layout()
plt.savefig("pirvision_corr_subset.png")
plt.close()

print("Explorarea datelor a fost realizata. Graficele si tabelele au fost salvate local.")

# --------------------
# Cerinta 3.2 - Preprocesarea Datelor
# --------------------

## 1. Tratarea valorilor lipsa

# Heart Dataset - identificare valori lipsa
heart_missing = heart_train.isna().sum()
heart_missing = heart_missing[heart_missing > 0].sort_values(ascending=False)

# Imputare univariata - folosim medie pentru numerice, moda pentru categorice
num_cols = heart_train.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = ['gender', 'education_level', 'smoking_status',
            'hypertension_history', 'stroke_history', 'diabetes_history',
            'blood_pressure_medication', 'high_blood_sugar']

num_imputer = SimpleImputer(strategy="mean")
cat_imputer = SimpleImputer(strategy="most_frequent")

heart_train[num_cols] = num_imputer.fit_transform(heart_train[num_cols])
heart_train[cat_cols] = cat_imputer.fit_transform(heart_train[cat_cols])

## 2. Identificarea si tratarea outlierilor

def remove_outliers_iqr(df, cols):
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[col] = np.where((df[col] < lower) | (df[col] > upper), np.nan, df[col])
    return df

# Aplicam doar pe coloane numerice
heart_train = remove_outliers_iqr(heart_train, num_cols)
heart_train[num_cols] = num_imputer.fit_transform(heart_train[num_cols])

## 3. Eliminarea atributelor redundante
# Eliminam ldl_cholesterol (corelat cu cholesterol_level) si sleep_heart_rate (corelat cu heart_rate)
heart_train.drop(columns=['ldl_cholesterol', 'sleep_heart_rate'], inplace=True)

# Actualizare lista coloane numerice
num_cols = [col for col in heart_train.select_dtypes(include=[np.number]).columns if col != "chd_risk"]

## 4. Standardizarea atributelor numerice
scaler = StandardScaler()
heart_train[num_cols] = scaler.fit_transform(heart_train[num_cols])

## PIRvision
# Tratare outlieri doar pentru OBS_1 (care are valori extreme)
pirvision_train['OBS_1'] = np.where(pirvision_train['OBS_1'] > pirvision_train['OBS_1'].quantile(0.99), 
                                    np.nan, pirvision_train['OBS_1'])

pirvision_train['OBS_1'] = pirvision_train['OBS_1'].fillna(pirvision_train['OBS_1'].mean())

# Standardizare a tuturor valorilor OBS
obs_cols = [col for col in pirvision_train.columns if col.startswith("OBS_")]
scaler_pir = StandardScaler()
pirvision_train[obs_cols] = scaler_pir.fit_transform(pirvision_train[obs_cols])

# Salvare date preprocesate
heart_train.to_csv("heart_train_preprocessed.csv", index=False)
pirvision_train.to_csv("pirvision_train_preprocessed.csv", index=False)

print("Cerinta 3.2 - Preprocesare completa: imputare, outlieri, redundanta, standardizare. Rezultatele au fost salvate.")


# --------------------
# Cerinta 3.3 - Utilizarea Algoritmilor de invatare automata
# --------------------

# 1. incarca datele
df = pd.read_csv("heart_train_preprocessed.csv")
X = df.drop(columns=["chd_risk"])
y = df["chd_risk"]

# 2. Functie pentru impartire corecta (cu ambele clase in y_test)
def stratified_split_with_class_check(X, y, test_size=0.2, max_tries=10):
    for i in range(max_tries):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=42 + i
        )
        if len(set(y_test)) == 2:
            print(f"✔️ Split valid gasit la incercarea {i + 1}")
            return X_train, X_test, y_train, y_test
    raise ValueError("Nu s-a putut obtine un set de test cu ambele clase.")

X_train, X_test, y_train, y_test = stratified_split_with_class_check(X, y)

# 3. Functie de evaluare
def evaluate_model(model, X_test, y_test, name):
    y_pred = model.predict(X_test)
    print(f"\n {name} - Classification Report")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

# 4. Decision Tree
dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, criterion='entropy', class_weight='balanced')
dt.fit(X_train, y_train)
evaluate_model(dt, X_test, y_test, "Decision Tree")

# 5. Random Forest
rf = RandomForestClassifier(n_estimators=100, max_depth=7, min_samples_leaf=4, class_weight='balanced', random_state=42)
rf.fit(X_train, y_train)
evaluate_model(rf, X_test, y_test, "Random Forest")

#6. Logistic Regression
lr = LogisticRegression(solver='lbfgs', max_iter=1000, class_weight='balanced')
lr.fit(X_train, y_train)
evaluate_model(lr, X_test, y_test, "Logistic Regression")

#7. MLP Classifier
mlp = MLPClassifier(hidden_layer_sizes=(64, 32), activation='relu',
                    solver='adam', alpha=0.001, max_iter=300, random_state=42)
mlp.fit(X_train, y_train)
evaluate_model(mlp, X_test, y_test, "MLP Classifier")
