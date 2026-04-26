import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords 
# Descarcarea pachetului stop_words
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    print("Pachetul 'stopwords' din NLTK nu a fost găsit. Se descarcă acum...")
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    print("Descărcare finalizată.")
    
# 1. PROCESAREA DATELOR

# Citirea setului de date
file_name = 'email_spam.xlsx'
sheet_name = 'Sheet1' 
df = None

try:
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    print(f"Citirea fisierului Excel '{file_name}' (foaia '{sheet_name}') a fost realizata cu succes!")
except FileNotFoundError:
    print(f"Eroare: Fisierul '{file_name}' nu a fost gasit. Asigurati-va ca este în aceeasi locatie cu scriptul.")
    exit()
except ImportError:
    print(f"Eroare: Va rugam sa instalati biblioteca openpyxl.")
    exit()
except Exception as e:
    print(f"A aparut o eroare la citirea fisierului: {e}")
    exit()

# Verificați structura setului de date
print("Verificare structura initiala")
print(df.head())
print("\n")

# Concatenarea si pregatirea coloanelor pentru pastrare a informatiei

# Redenumim temporar pentru claritate, bazat pe structura v1, v2, Unnamed: 2, etc.
# Ne asiguram că DataFrame-ul are cel putin 5 coloane
if df.shape[1] >= 5:
    df.columns = ['label', 'message', 'extra1', 'extra2', 'extra3']
    # Umplem valorile lipsa (NaN) cu siruri de caractere goale
    df[['extra1', 'extra2', 'extra3']] = df[['extra1', 'extra2', 'extra3']].fillna('')
    # Concatenam continutul coloanelor suplimentare la coloana 'message'
    df['message'] = df['message'].astype(str) + ' ' + df['extra1'].astype(str) + ' ' + df['extra2'].astype(str) + ' ' + df['extra3'].astype(str)
    # Eliminam coloanele suplimentare
    df = df.drop(columns=['extra1', 'extra2', 'extra3'])
    df.columns = ['label', 'message']
    
else:
    # Daca fisierul Excel nu avea coloanele suplimentare, ne asiguram ca numele sunt corecte
    df.columns = ['label', 'message']
    print("Fisierul nu continea coloane suplimentare, doar 'label' și 'message' (v1 și v2).")


df['message'] = df['message'].str.strip() # Curatam spatiile suplimentare

print("Structura dupa concatenarea datelor")
print(df.head())
print("\n")

# Verificare si eliminare duplicatele din dataset
initial_rows = len(df)
duplicate_count = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"Eliminarea duplicatelor")
print(f"Numar de randuri initiale: {initial_rows}")
print(f"Numar de duplicate gasite si eliminate: {duplicate_count}")
print(f"Numar de randuri dupa eliminarea duplicatelor: {len(df)}")
print("\n")

df['label'] = df['label'].map({'ham': 0, 'spam': 1})
print(f"Distributia variabilei tinta (0=ham, 1=spam)")
print(df['label'].value_counts())
print("\n")

# Vizualizare distributie variabila tinta
plt.figure(figsize=(6, 4))
df['label'].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Distributia Claselor (Ham vs. Spam)')
plt.xlabel('Clasa (0: Ham, 1: Spam)')
plt.ylabel('Numar de mesaje')
plt.xticks(ticks=[0, 1], labels=['Ham', 'Spam'], rotation=0)
plt.show()
plt.savefig("Distributia Claselor (Ham vs. Spam).png")

# Metoda de curatare a textului
def clean_text(text):
    # Convertim explicit la string
    text = str(text).lower() 
    # Eliminarea semnelor de punctuatie
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Eliminarea cifrelor 
    text = re.sub(r'\d+', '', text)
    # Eliminarea cuvintelor stop 
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['message_cleaned'] = df['message'].apply(clean_text)
print("Exemplu de mesaje curatate:")
print(df[['message', 'message_cleaned']].head(2).to_markdown(index=False))
print("\n")

# 2. Antrenarea si evaluarea modelelor

# Separarea caracteristicile (X) de variabila tinta (y)
X = df['message_cleaned']
y = df['label']

# Impartirea datele in seturi de antrenament si testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Split Date (Antrenament/Testare)")
print(f"Set de antrenament: {X_train.shape[0]} ({y_train.value_counts(normalize=True)[1]:.2%} spam)")
print(f"Set de testare: {X_test.shape[0]} ({y_test.value_counts(normalize=True)[1]:.2%} spam)")
print("\n")

# Model 1: Multinomial Naive Bayes (MNB)
pipeline_mnb = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB()),
])

param_grid_mnb = {
    'tfidf__ngram_range': [(1, 1), (1, 2)], 
    'tfidf__max_df': [0.75, 1.0],
    'clf__alpha': [0.1, 0.5, 1.0],          
}

# Antrenare mai multe modele de clasificare cu diferite combinatii de hiperparametri (MNB)
print("GridSearchCV: Multinomial Naive Bayes (Optimizare Hiperparametri)")
grid_search_mnb = GridSearchCV(pipeline_mnb, param_grid_mnb, cv=5, scoring='f1', n_jobs=-1)
grid_search_mnb.fit(X_train, y_train)
best_mnb = grid_search_mnb.best_estimator_
print(f"Cei mai buni hiperparametri MNB: {grid_search_mnb.best_params_}")
print("\n")

# Model 2: Regresie Logistica (LogReg)
pipeline_logreg = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(solver='liblinear', random_state=42, max_iter=1000)),
])

param_grid_logreg = {
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'tfidf__max_df': [0.75, 1.0],
    'clf__C': [0.1, 1, 10],                 
    'clf__penalty': ['l1', 'l2'],           
}

# Antrenare mai multe modele de clasificare cu diferite combinatii de hiperparametri (LogReg)
print("GridSearchCV: Regresie Logistica (Optimizare Hiperparametri)")
grid_search_logreg = GridSearchCV(pipeline_logreg, param_grid_logreg, cv=5, scoring='f1', n_jobs=-1)
grid_search_logreg.fit(X_train, y_train)
best_logreg = grid_search_logreg.best_estimator_
print(f"Cei mai buni hiperparametri LogReg: {grid_search_logreg.best_params_}")
print("\n")

# Evaluare fiecare tip de model cu cea mai buna combinatie de hiperparametri

print("RAPORT DE CLASIFICARE: Multinomial Naive Bayes (Optimizat)")
y_pred_mnb = best_mnb.predict(X_test)
print(classification_report(y_test, y_pred_mnb, target_names=['Ham (0)', 'Spam (1)']))


print("RAPORT DE CLASIFICARE: Regresie Logistica (Optimizata)")
y_pred_logreg = best_logreg.predict(X_test)
print(classification_report(y_test, y_pred_logreg, target_names=['Ham (0)', 'Spam (1)']))



# Afisare matricea de confuzie pentru fiecare tip de model sub forma de grafic
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Matricile de Confuzie pentru Modelele Optimizate', fontsize=16)

# Matricea de confuzie pentru MNB
cm_mnb = confusion_matrix(y_test, y_pred_mnb)
disp_mnb = ConfusionMatrixDisplay(confusion_matrix=cm_mnb, display_labels=['Ham', 'Spam'])
disp_mnb.plot(cmap=plt.cm.Blues, ax=axes[0])
axes[0].title.set_text(f'Multinomial Naive Bayes (F1-Score: {grid_search_mnb.best_score_:.4f})')

# Matricea de confuzie pentru LogReg
cm_logreg = confusion_matrix(y_test, y_pred_logreg)
disp_logreg = ConfusionMatrixDisplay(confusion_matrix=cm_logreg, display_labels=['Ham', 'Spam'])
disp_logreg.plot(cmap=plt.cm.Blues, ax=axes[1])
axes[1].title.set_text(f'Regresie Logistica (F1-Score: {grid_search_logreg.best_score_:.4f})')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("Matricile de Confuzie pentru Modelele Optimizate.png")
plt.show()

output_file_name = 'email_spam_procesat.xlsx'
sheet_name = 'Date_Curatate'
try:
    df.to_excel(output_file_name, sheet_name=sheet_name, index=False)
    print(f"Datele procesate au fost salvate cu succes in: {output_file_name}")

except Exception as e:
    print(f"A aparut o eroare la salvarea fisierului Excel: {e}")