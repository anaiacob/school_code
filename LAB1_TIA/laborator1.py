import pandas as pd
from typing import Optional, Tuple, Dict, Any, List
import numpy as np
import warnings
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from imblearn.over_sampling import SMOTE
from collections import Counter

# Suprima avertismentele de tip SettingWithCopyWarning si altele
warnings.filterwarnings('ignore')

# Definitii Globale
FILE_PATH = "dataset_laborator_1.xlsx"
TARGET_COLUMN = "amount_bought" 
TG_COLUMN = "wine_id"

# Incarcare Date
try:
    df = pd.read_excel(FILE_PATH)
    if df.empty:
        raise ValueError("DataFrame-ul incarcat este gol.")
except FileNotFoundError:
    print(f"Eroare: Fisierul '{FILE_PATH}' nu a fost gasit.")
    df = pd.DataFrame()
except ValueError as e:
    print(f"Eroare la incarcare: {e}")
    df = pd.DataFrame()


# CERINTA 1.1: GESTIONAREA VALORILOR LIPSA (Pastrate ca in original)

def cerinta1(df: pd.DataFrame) -> pd.DataFrame:
    """Afiseaza coloanele cu valori lipsa si procentajul lor."""
    print("\n" + "="*50)
    print("CERINTA 1.1 (PAS 1): ANALIZA VALORILOR LIPSA")
    print("="*50)
    
    missing_info = pd.DataFrame({
        'Valori Lipsa (Count)': df.isnull().sum(),
        'Procent Lipsa (%)': (df.isnull().sum() / len(df)) * 100
    })
    missing_info = missing_info[missing_info['Valori Lipsa (Count)'] > 0].sort_values(
        by='Procent Lipsa (%)', ascending=False
    )
    
    nr_col_miss_val = len(missing_info)
    
    if nr_col_miss_val > 0:
        print("Coloane cu valori lipsa si procentaje:")
        print(missing_info.style.format({'Procent Lipsa (%)': '{:.2f}%'}).to_string())
    else:
        print("Nu au fost gasite coloane cu valori lipsa.")
        
    print(f"\nNumarul total de coloane cu valori lipsa: {nr_col_miss_val}")
    return df


def drop_high_missing_row(df: pd.DataFrame, threshold: float = 0.35) -> pd.DataFrame:
    """Elimina randurile cu % missing > threshold."""
    initial_rows = len(df)
    df = df[df.isna().mean(axis=1) <= threshold].copy()
    
    print(f"\nCERINtA 1.1 (PAS 2): Eliminat {initial_rows - len(df)} randuri cu procent de lipsa > {threshold*100:.0f}%. Randuri ramase: {len(df)}")
    return df


def impute_missing(df: pd.DataFrame,
                   strategy_num: str = "median",
                   strategy_cat: str = "mode",
                   fill_value: Optional[Any] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Completeaza valorile lipsa si returneaza statisticile folosite."""
    stats = {}
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    for c in num_cols:
        if df[c].isna().any():
            val = df[c].median() if strategy_num == "median" else df[c].mean()
            df[c].fillna(val, inplace=True)
            stats[c] = f"{strategy_num}: {val:.4f}"
    
    for c in cat_cols:
        if df[c].isna().any():
            val = df[c].mode().iloc[0] if strategy_cat == "mode" and not df[c].mode().empty else "missing"
            df[c].fillna(val, inplace=True)
            stats[c] = f"{strategy_cat}: {val}"

    print(f"\nCERINtA 1.1 (PAS 3): Imputare finalizata. Coloane imputate si valori folosite:")
    print(pd.Series(stats).to_string())
    print("="*50 + "\n")
    return df, stats

# CERINTA 1.2: ELIMINAREA DATELOR REDUNDANTE

def drop_redundant_data(df: pd.DataFrame, target_col: str, 
                        corr_target_thresh: float = 0.99, 
                        unique_thresh: float = 0.95, 
                        corr_inter_thresh: float = 0.85, 
                        var_thresh: float = 0.05) -> pd.DataFrame:
    df_curatat = df.copy()
    initial_shape = df_curatat.shape

    # 3. Elimina randurile duplicate
    initial_rows = len(df_curatat)
    df_curatat.drop_duplicates(inplace=True)
    print(f"Randuri eliminate (Duplicate): {initial_rows - len(df_curatat)}. Ramase: {len(df_curatat)}")

    # 2. Elimina coloanele cu identificatori unici
    cols_to_drop_id = [c for c in df_curatat.columns 
                    if df_curatat[c].nunique() / len(df_curatat) > unique_thresh]
    df_curatat.drop(columns=cols_to_drop_id, inplace=True, errors='ignore')
    print(f"Coloane eliminate (Identificatori > {unique_thresh}): {cols_to_drop_id}")
    
    # Re-actualizare (I): Coloane numerice predictive curente
    num_pred_cols = [c for c in df_curatat.select_dtypes(include=np.number).columns if c != target_col]
    
    if num_pred_cols:
        # 5. Elimina coloanele cu varianța aproape zero
        variances = df_curatat[num_pred_cols].var()
        cols_to_drop_var = variances[variances < var_thresh].index.tolist()
        df_curatat.drop(columns=cols_to_drop_var, inplace=True, errors='ignore')
        print(f"Coloane eliminate (Varianta mica < {var_thresh}): {cols_to_drop_var}")
        
        # Re-actualizare (II): Dupa eliminarea varianței mici
        num_pred_cols = [c for c in df_curatat.select_dtypes(include=np.number).columns if c != target_col]

        # 4. Elimina caracteristicile puternic corelate inter-caracteristici
        if num_pred_cols:
            corr_matrix = df_curatat[num_pred_cols].corr().abs()
            upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            cols_to_drop_corr = [col for col in upper.columns if any(upper[col] > corr_inter_thresh)]
            df_curatat.drop(columns=cols_to_drop_corr, inplace=True, errors='ignore')
            print(f"Coloane eliminate (Corelatie inter-caracteristici > {corr_inter_thresh}): {cols_to_drop_corr}")

            # Re-actualizare (III): Dupa eliminarea corelațiilor inter-caracteristici (Fixeaza KeyError)
            num_pred_cols = [c for c in df_curatat.select_dtypes(include=np.number).columns if c != target_col]

            # 1. Elimina coloanele puternic corelate cu targetul
            if target_col in df_curatat.columns:
                correlations = df_curatat[num_pred_cols].corrwith(df_curatat[target_col]).abs()
                cols_to_drop_target = correlations[correlations >= corr_target_thresh].index.tolist()
                df_curatat.drop(columns=cols_to_drop_target, inplace=True, errors='ignore')
                print(f"Coloane eliminate (Corelatie cu Target > {corr_target_thresh}): {cols_to_drop_target}")

    print(f"\nForma Initiala: {initial_shape}, Forma Finala: {df_curatat.shape}")
    return df_curatat

# CERINTA 1.3: IDENTIFICAREA OUTLIERILOR

def handle_outliers(df: pd.DataFrame, action: str = 'capping') -> pd.DataFrame:
    """Implementeaza CERINTA 1.3: Vizualizare si gestionare."""
    print("\n" + "="*50)
    print("CERINTA 1.3: GESTIONAREA OUTLIERILOR")
    print("="*50)
    df_out = df.copy()
    num_cols = [c for c in df_out.select_dtypes(include=np.number).columns.tolist() if c != TARGET_COLUMN]
    
    # 1. Vizualizare (Boxplot pentru primele 3 coloane numerice)
    cols_to_plot = num_cols[:min(3, len(num_cols))]
    if cols_to_plot:
        print(f"Vizualizare: Boxplot pentru {cols_to_plot}.")
        df_out[cols_to_plot].plot(kind='box', subplots=True, layout=(1, len(cols_to_plot)), figsize=(15, 5))
        plt.show()
        plt.savefig(f"Boxplot {cols_to_plot}")
    
    # 2. & 3. Detectare (IQR & Z-score)
    outlier_count = 0
    for col in num_cols:
        Q1, Q3 = df_out[col].quantile(0.25), df_out[col].quantile(0.75)
        IQR = Q3 - Q1
        lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
        outliers = df_out.index[(df_out[col] < lower) | (df_out[col] > upper)].tolist()
        outlier_count += len(outliers)
        
    print(f"\nDetectat un total de {outlier_count} outlieri unici (metoda IQR, k=1.5).")

    # 4. Actiune asupra outlierilor (Capping, Drop, etc.)
    if action == 'capping':
        print(f"Actiune: Aplicare CAPPING (limitare) pe baza IQR.")
        rows_affected = 0
        for col in num_cols:
            Q1, Q3 = df_out[col].quantile(0.25), df_out[col].quantile(0.75)
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            
            rows_affected += (df_out[col] < lower).sum() + (df_out[col] > upper).sum()
            df_out[col] = np.where(df_out[col] < lower, lower, df_out[col])
            df_out[col] = np.where(df_out[col] > upper, upper, df_out[col])
        print(f"Numar de valori limitate (capping): Aproximativ {rows_affected}")

    elif action == 'drop':
        # Implementare simpla, se poate imbunatati
        print(f"Actiune: Eliminare (DROP) a randurilor cu outlieri (bazat pe IQR). Sarit peste pentru a mentine flow-ul.")

    print(f"Forma finala dupa gestionarea outlierilor: {df_out.shape}")
    print("="*50 + "\n")
    return df_out


# CERINTA 1.4: CODIFICAREA CARACTERISTICILOR CATEGORICE

def encode_categorical_features(df: pd.DataFrame, 
                               ordinal_cols: List[str], 
                               high_cardinality_cols: List[str]) -> pd.DataFrame:
    """Implementeaza toti pasii din CERINTA 1.4."""
    print("\n" + "="*50)
    print("CERINTA 1.4: CODIFICAREA CARACTERISTICILOR CATEGORICE")
    print("="*50)
    df_encoded = df.copy()
    
    cat_cols_initial = df_encoded.select_dtypes(include=["object", "category"]).columns.tolist()
    print(f"Categorice initiale: {cat_cols_initial}")

    # 1. Label Encoding (pentru variabile ordinale)
    for col in ordinal_cols:
        if col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[col + '_LE'] = le.fit_transform(df_encoded[col].astype(str))
            df_encoded.drop(columns=[col], inplace=True)
            print(f"Aplicat Label Encoding pe: {col}")
            if col in cat_cols_initial: cat_cols_initial.remove(col) 
    
    # 2. Target Encoding (pentru variabile cu cardinalitate mare)
    for col in high_cardinality_cols:
        if col in df_encoded.columns and TARGET_COLUMN in df_encoded.columns:
            target_means = df_encoded.groupby(col)[TARGET_COLUMN].mean()
            df_encoded[col + '_TE'] = df_encoded[col].map(target_means)
            df_encoded.drop(columns=[col], inplace=True)
            print(f"Aplicat Target Encoding pe: {col}")
            if col in cat_cols_initial: cat_cols_initial.remove(col)
    
    # 3. One-Hot Encoding (pentru variabile nominale ramase)
    nominal_cols = [col for col in cat_cols_initial if col in df_encoded.columns]
    if nominal_cols:
        df_encoded = pd.get_dummies(df_encoded, columns=nominal_cols, prefix=nominal_cols)
        print(f"Aplicat One-Hot Encoding pe {len(nominal_cols)} coloane nominale.")
        print(f"Exemplu de coloane noi: {list(df_encoded.columns)[-5:]}")

    print(f"Forma finala dupa codificare: {df_encoded.shape}")
    print("="*50 + "\n")
    return df_encoded


# CERINTA 1.5: SCALAREA CARACTERISTICILOR

def scale_features(df: pd.DataFrame, scaling_method: str = 'standard') -> pd.DataFrame:
    """Aplica StandardScaler sau MinMaxScaler pe coloanele numerice."""
    print("\n" + "="*50)
    print("CERINTA 1.5: SCALAREA CARACTERISTICILOR")
    print("="*50)
    df_scaled = df.copy()
    
    num_cols = [c for c in df_scaled.select_dtypes(include=np.number).columns.tolist() if c != TARGET_COLUMN]
    
    if not num_cols:
        print("Nu s-au gasit coloane numerice de scalat.")
        return df_scaled
    
    if scaling_method == 'standard':
        scaler = StandardScaler()
        print("Aplicat StandardScaler (Normalizare Z-score).")
    elif scaling_method == 'minmax':
        scaler = MinMaxScaler()
        print("Aplicat MinMaxScaler (Scalare [0,1]).")
    else:
        raise ValueError("scaling_method trebuie sa fie 'standard' sau 'minmax'.")
        
    df_scaled[num_cols] = scaler.fit_transform(df_scaled[num_cols])
    
    print(f"Primele 3 coloane scalate si valorile lor (dupa scalare):")
    print(df_scaled[num_cols[:3]].head())
    print("="*50 + "\n")
    return df_scaled


# CERINTA 1.6: GESTIONAREA DATELOR DEZECHILIBRATE

def balance_data(df: pd.DataFrame, target_col: str, sampling_method: str = 'smote') -> pd.DataFrame:
    """Implementeaza CERINTA 1.6."""
    print("\n" + "="*50)
    print("CERINTA 1.6: GESTIONAREA DATELOR DEZECHILIBRATE")
    print("="*50)
    
    if target_col not in df.columns or df[target_col].nunique() < 2 or df[target_col].nunique() > 50:
        print(f"Sarit peste balansare: Coloana tinta lipseste sau nu este de clasificare.")
        print("="*50 + "\n")
        return df

    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # 1. Analiza distributiei claselor
    class_counts = y.value_counts()
    print("Distributia initiala a claselor:")
    print(class_counts.to_string())
    
    # Vizualizare (optional)
    class_counts.plot(kind='bar'); 
    plt.title('Distributia Claselor'); 
    plt.show() 
    plt.savefig("Distributia Claselor")

    # 2. Aplica tehnici de sampling
    if sampling_method == 'smote':
        sampler = SMOTE(random_state=42)
        print("\nAplicat SMOTE (Over-sampling) pentru a egaliza clasele.")
    else: # undersampling
        sampler = RandomUnderSampler(random_state=42)
        print("\nAplicat Random Under-sampling.")

    try:
        X_res, y_res = sampler.fit_resample(X, y)
        df_balanced = pd.concat([X_res, y_res], axis=1)
        
        print("Distributia claselor dupa sampling:")
        print(pd.Series(y_res).value_counts().to_string())
        print(f"Forma finala dupa balansare: {df_balanced.shape} (Initiala: {df.shape})")
        return df_balanced
        
    except ValueError as e:
        print(f"\nEroare la aplicarea sampling-ului. Asigura-te ca datele sunt numerice: {e}")
        return df
    finally:
        print("="*50 + "\n")

if __name__ == "__main__":
    if 'df' in locals() and not df.empty:
        
        df_processed = df.copy()

        # 1. GESTIONAREA VALORILOR LIPSA (1.1)
        df_processed = cerinta1(df_processed) 
        df_processed = drop_high_missing_row(df_processed, threshold=0.35)
        df_processed, _ = impute_missing(df_processed, strategy_num="median", strategy_cat="mode")

        # 2. ELIMINAREA DATELOR REDUNDANTE (1.2)
        df_processed = drop_redundant_data(df_processed, target_col=TG_COLUMN)

        # 3. GESTIONAREA OUTLIERILOR (1.3)
        df_processed = handle_outliers(df_processed, action='capping') 

        # 4. CODIFICAREA CATEGORICELOR (1.4)
        df_processed = encode_categorical_features(
            df_processed, 
            ordinal_cols=[],
            high_cardinality_cols=[]
        )

        # 5. SCALAREA CARACTERISTICILOR (1.5)
        df_processed = scale_features(df_processed, scaling_method='standard')

        # 6. GESTIONAREA DATELOR DEZECHILIBRATE (1.6)
        df_processed = balance_data(df_processed, target_col=TARGET_COLUMN, sampling_method='smote')
        print(df_processed.columns)
        print("\n" + "="*50)
        print("PROCESARE COMPLETA FINALIZATA!")
        print(f"Forma finala a DataFrame-ului: {df_processed.shape}")
        print("="*50)

    else:
        print("\nNu se poate continua procesarea deoarece DataFrame-ul este gol sau nu a putut fi incarcat.")