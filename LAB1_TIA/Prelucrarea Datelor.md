# Prelucrarea datelor

## 1. Prelucrarea datelor tabelare

### 1.1: Tratarea valorilor lipsă
- Identifică coloanele cu valori lipsă și calculează procentajul de valori lipsă pentru fiecare coloană
- Aplică strategii diferite: eliminare rânduri/coloane cu multe valori nule (> 0.35), completare cu medie/mediană

### 1.2: Eliminarea datelor redundante
- Identifică și elimină coloanele puternic corelate cu targetul
- Identifică și elimină coloanele cu identificatori unici
- Identifică și elimină rândurile duplicate
- Calculează matricea de corelație și elimină caracteristicile puternic corelate (> 0.85)
- Elimină coloanele cu varianță aproape zero (< 0.05)

### 1.3: Identificarea outlierilor
- Vizualizează distribuția datelor folosind boxplot
- Detectează outlierii folosind metoda IQR (Interquartile Range)
- Detectează outlierii folosind metoda Z-score
- Eliminare, transformare sau păstrare a outlierilor

### 1.4: Codificarea caracteristicilor categorice
- Identifică coloanele categorice din dataset
- Aplică Label Encoding pentru variabilele ordinale
- Aplică One-Hot Encoding pentru variabilele nominale
- Opțional: Aplică Target Encoding pentru variabile cu cardinalitate mare

### 1.5: Scalarea caracteristicilor
- Aplică StandardScaler (z-score normalization) pe caracteristicile numerice
- Aplică MinMaxScaler pentru scalare în intervalul [0,1]

### 1.6: Gestionarea datelor dezechilibrate
- Analizează distribuția claselor într-un dataset de clasificare (folosiți bar-plot)
- Aplică tehnici de under-sampling sau over-sampling pentru balansarea distribuției claselor

---

## 2. Prelucrarea textului

### 2.1: Preprocesarea de bază a textului
- Aplică lowercase transformation
- Elimină semnele de punctuație și caractere speciale
- Elimină spații albe excesive și caracterele '/n'

### 2.2: Tokenizare și eliminarea stopwords
- Tokenizează textul în cuvinte folosind nltk sau spacy
- Încarcă lista de stopwords pentru limba română
- Elimină stopwords din text

### 2.3: Stemming și Lemmatizatizare
- Aplică stemming si lemmantizare
- Hint: Folosiți librăria 'simplemma' - le face pe amândouă

### 2.4: Vectorizarea textului
- Impărțiți textul in paragrafe
- Aplicați TF-IDF pe paragrafele respective.
- Optional: Pune-ți o întrebare și încercați sa faceți un 'Information Retrieval'

---

## 3. Prelucrarea imaginilor

### 3.1: Vizualizarea imaginilor
- Afișează dimensiunile, numărul de canale și imaginea data

### 3.2: Redimensionarea imaginilor
- Redimensionează imaginea (ex: 224x224)

### 3.3: Normalizarea pixelilor
- Scalează valorile pixelilor de la [0, 255] la [0, 32]
- Binarizează imaginea

### 3.4: Augmentarea datelor de imagine
- Aplică rotații aleatorii (±15 grade)
- Aplică flip orizontal/vertical
- Modifică luminozitatea și contrastul
- Aplică zoom și crop aleatoriu
- Opțional: Încercați combinații de augmentări

### 3.5: Conversia spațiilor de culoare
- Convertește imagini color în grayscale
- Opțional: Experimentează cu alte spații de culoare (ex: HSV)