import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

file_name = "salary.csv"
df = None

df = pd.read_csv(file_name)

# CERINTA 1. PROCESAREA DATELOR

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
print(df["Salary"].value_counts())
print('\n')

# Pentru Random Forest, care nu accepta alte valori decat numerice
label_encoders = {}

for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

numeric_cols = df.select_dtypes(include=np.number).columns

# Eliminarea valorilor puternic corelate
corr_matrix = df.select_dtypes(include=np.number).corr()
plt.figure(figsize=(12, 8))
sns.heatmap(
    corr_matrix,
    cmap="coolwarm",
    annot=True,
    fmt=".2f"
)
plt.title("Matricea de corelatie")
plt.show()

df = df.drop(columns="Age")

# Histograme

plt.figure(figsize=(6, 4))
plt.hist(df["Salary"], bins=20)
plt.title("Distributia salariului")
plt.xlabel("Salary")
plt.ylabel("Frecventa")
plt.show()

plt.figure(figsize=(6, 4))
plt.hist(df["Years of Experience"], bins=20)
plt.title("Distributia anilor de experienta")
plt.xlabel("Years of Experience")
plt.ylabel("Frecventa")
plt.show()
# Histograma distributiei Salary pe Gender
male_salary = df[df["Gender"] == 1]["Salary"]
female_salary = df[df["Gender"] == 0]["Salary"]

plt.figure(figsize=(7, 5))
plt.hist(male_salary, bins=20, alpha=0.6, label="Male")
plt.hist(female_salary, bins=20, alpha=0.6, label="Female")

plt.title("Distributia Salary pe Gender")
plt.xlabel("Salary")
plt.ylabel("Frecventa")
plt.legend()
plt.show()

# Histograma distributiei Years of Experience pe Gender
male_exp = df[df["Gender"] == 1]["Years of Experience"]
female_exp = df[df["Gender"] == 0]["Years of Experience"]

plt.figure(figsize=(7, 5))
plt.hist(male_exp, bins=20, alpha=0.6, label="Male")
plt.hist(female_exp, bins=20, alpha=0.6, label="Female")

plt.title("Distributia Years of Experience pe Gender")
plt.xlabel("Years of Experience")
plt.ylabel("Frecventa")
plt.legend()
plt.show()

# CERINTA 2. MODELE DE REGRESIE DE TIP ARBORE

X = df.drop(columns=["Salary"])
y = df["Salary"]
# Impartirea in set de antrenament si test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Antrenarea si evaluarea modelelor
model_results = []
# RANDOM FOREST REGRESSOR
print("\nRANDOM FOREST REGRESSOR\n")
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
    rf = RandomForestRegressor(**config)
    # Antrenarea modelului
    rf.fit(X_train, y_train)
    # Predictii pe setul de test
    y_pred = rf.predict(X_test)
    # Calcularea metricilor
    mae = mean_absolute_error(y_test,y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    # Salvarea rezultatelor
    results.append({
        "Model": i,
        "MAE": mae,
        "MSE": mse,
        "R2 Score": r2
    })
    # Afisarea rezultatelor
    print("MAE", mae)
    print("MSE:", mse)
    print("R2 Score:", r2)
    

# Compararea modelelor și alegerea celui mai bun
results_df = pd.DataFrame(results)

print("\n           REZULTATE FINALE            ")
print(results_df)

best_model = results_df.loc[results_df["R2 Score"].idxmax()]

print("\n           CEL MAI BUN MODEL Random Forest(după R2)            ")
print(best_model)

model_results.append(
    {
        "Regressor": "Random Forest",
        "Model": best_model["Model"],
        "MAE": best_model["MAE"],
        "MSE": best_model["MSE"],
        "R2 Score": best_model["R2 Score"]
    }
)

# DECISION TREE REGRESSOR
print("\nDECISION TREE REGRESSOR\n")
dt_configs = [
    {
        "max_depth":5,
        "min_samples_split":10,
        "random_state":42,
        "min_samples_leaf": 2
    },
    {
        "max_depth":10,
        "min_samples_split":5,
        "random_state":42,
        "min_samples_leaf": 1
    },
    {
        "max_depth":15,
        "min_samples_split":5,
        "random_state":42,
        "min_samples_leaf": 4
    }
]

resultsdt=[]

for i, config in enumerate(dt_configs, start=1):
    print(f"\n           Model {i}           ")
    # Initializarea modelului Decision Tree
    dt = DecisionTreeRegressor(**config)
    # Antrenarea modelului
    dt.fit(X_train, y_train)
    # Predictii pe setul de test
    y_pred = dt.predict(X_test)
    # Calcularea metricilor
    mae = mean_absolute_error(y_test,y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    # Salvarea rezultatelor
    resultsdt.append({
        "Model": i,
        "MAE": mae,
        "MSE": mse,
        "R2 Score": r2
    })
    # Afisarea rezultatelor
    print("MAE", mae)
    print("MSE:", mse)
    print("R2 Score:", r2)
    
# Compararea modelelor și alegerea celui mai bun
results_dt = pd.DataFrame(resultsdt)

print("\n           REZULTATE FINALE            ")
print(results_dt)

best_model_dt = results_dt.loc[results_dt["R2 Score"].idxmax()]

print("\n           CEL MAI BUN MODEL Decision Tree(după R2)            ")
print(best_model_dt)


model_results.append(
    {
        "Regressor": "Decision Tree",
        "Model": best_model_dt["Model"],
        "MAE": best_model_dt["MAE"],
        "MSE": best_model_dt["MSE"],
        "R2 Score": best_model_dt["R2 Score"]
    }
)

# GRADIENT BOOSTING REGRESSOR
print("\nGRADIENT BOOSTING REGRESSOR\n")
gb_configs = [
    {
        "max_depth":4,
        "learning_rate":0.1,
        "random_state":42,
        "n_estimators": 100
    },
    {
        "max_depth":3,
        "learning_rate":0.05,
        "random_state":42,
        "n_estimators": 200
    },
    {
        "max_depth":5,
        "learning_rate":0.05,
        "random_state":42,
        "n_estimators": 300
    }
]

resultsgb=[]

for i, config in enumerate(gb_configs, start=1):
    print(f"\n           Model {i}           ")
    # Initializarea modelului Decision Tree
    gb = GradientBoostingRegressor(**config)
    # Antrenarea modelului
    gb.fit(X_train, y_train)
    # Predictii pe setul de test
    y_pred = gb.predict(X_test)
    # Calcularea metricilor
    mae = mean_absolute_error(y_test,y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    # Salvarea rezultatelor
    resultsgb.append({
        "Model": i,
        "MAE": mae,
        "MSE": mse,
        "R2 Score": r2
    })
    # Afisarea rezultatelor
    print("MAE", mae)
    print("MSE:", mse)
    print("R2 Score:", r2)
    
# Compararea modelelor și alegerea celui mai bun
results_gb = pd.DataFrame(resultsgb)

print("\n           REZULTATE FINALE            ")
print(results_gb)

best_model_gb = results_gb.loc[results_gb["R2 Score"].idxmax()]

print("\n           CEL MAI BUN MODEL Gradient Boosting(după R2)            ")
print(best_model_gb)


model_results.append(
    {
        "Regressor": "Gradient Boosting",
        "Model": best_model_gb["Model"],
        "MAE": best_model_gb["MAE"],
        "MSE": best_model_gb["MSE"],
        "R2 Score": best_model_gb["R2 Score"]
    }
)


result_mdl = pd.DataFrame(model_results)
bst_mdl = result_mdl.loc[result_mdl["R2 Score"].idxmax()]
print("\n           CEL MAI BUN MODEL (după R2)            ")
print(bst_mdl)