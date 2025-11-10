import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import os

csv_path = "C:\\Users\\anaia\\Downloads\\Laborator 2 TIA\\houses.csv"
current_year = 2025
RANDOM_STATE = 42

df = pd.read_csv(csv_path)
# CERINTA 1. PRELUCRAREA DATELOR

# Adaugarea coloanei Years_Since_Built
df["Years_Since_Built"]=current_year-df["Year_Built"]

# Normalizarea min-max pt Square_Footage
sq_scaler = MinMaxScaler()
df["Square_Footage_Norm"] = sq_scaler.fit_transform(df[["Square_Footage"]])

df.to_csv("houses_with_years.csv", index=False)

# CERINTA 2. PREGATIREA DATELOR PENTRU ANTRENARE
# Separarea caracteristicilor
feature_cols = [
    "Square_Footage_Norm",
    "Num_Bedrooms",
    "Num_Bathrooms",
    "Lot_Size",
    "Garage_Size",
    "Neighborhood_Quality",
    "Years_Since_Built",
]

x = df[feature_cols]
y = df["House_Price"]

# Impartirea datelor in seturi de antrenament si testare
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=RANDOM_STATE
)

# CERINTA 3. ANTRENAREA MODELULUI
# LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(x_train,y_train)

# SGDRegressor

sgd_pip = Pipeline([
    ("scaler", StandardScaler()),
    (
        "sgd", SGDRegressor(
            max_iter= 10000,
            tol = 1e-6,
            learning_rate = "invscaling",
            eta0 = 0.01,
            random_state = RANDOM_STATE,
            penalty = "l2"
        )
    )
])

sgd_pip.fit(x_train,y_train)

# CERINTA 4. EVALUAREA MODELULUI
# Predictie LinearRegression
y_pred_lin = lin_reg.predict(x_test)
# Predictie SGDRegressor
y_pred_sgd = sgd_pip.predict(x_test)

# Metrici
mse_lin = mean_squared_error(y_test, y_pred_lin)
r2_lin = r2_score(y_test, y_pred_lin)

mse_sgd = mean_squared_error(y_test, y_pred_sgd)
r2_sgd = r2_score(y_test, y_pred_sgd)

print("Evaluare modele", end="\n")
print("LinearRegression", end="\n")
print(f"mse: {mse_lin}, r2: {r2_lin}", end="\n")
print("SGDRegressor", end="\n")
print(f"mse: {mse_sgd}, r2: {r2_sgd}", end="\n")

# CERINTA 5. VIZUALIZAREA REZULTATELOR

def real_vs_pred(y_true, y_pred, title, file_name=None)->None:
    plt.figure(figsize=(10,10))
    plt.scatter(y_true, y_pred, alpha=0.6)
    minv = min(y_true.min(), y_pred.min())
    maxv = max(y_true.max(), y_pred.max())
    plt.plot([minv, maxv], [minv, maxv])
    plt.xlabel("Pret real")
    plt.ylabel("Pret prezis")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    if file_name:
        plt.savefig(file_name, dpi=150)
    plt.show()
    
real_vs_pred(y_test, y_pred_lin, "LinearRegression: Real vs Prezis", "linreg_real_vs_pred.png")
real_vs_pred(y_test, y_pred_sgd, "SGDRegressor: Real vs Prezis", "sgd_real_vs_pred.png")
