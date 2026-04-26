import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler

# CERINTA 1
# Verificarea setului de date
df = pd.read_csv("iris.csv", index_col=0)

print("Primele 5 rânduri ale datasetului:")
print(df.head())

# 1.2. Verificarea structurii datasetului
print("\nInformatii despre dataset:")
print(df.info())

# 1.3. Verificarea valorilor lipsa
print("\nNumar valori lipsa pe coloana:")
print(df.isnull().sum())

# 1.4. Statistici descriptive
print("\nStatistici descriptive:")
print(df.describe())

# 1.5. Verificarea distributiei valorilor pentru coloana 'species'
print("\nDistribuția speciilor:")
print(df['species'].value_counts())

# 1.6. Verificarea duplicatelor
print("\nNumar de randuri duplicate:")
print(df.duplicated().sum())

# Verificarea distributiei clusterelor (speciilor reale)
plt.figure()
counts = df['species'].value_counts()
counts.plot(kind='bar')
plt.title("Distributia speciilor")

for i, value in enumerate(counts):
    plt.text(i, value + 0.5, str(value), ha='center', fontsize=12)

plt.xlabel("Specie")
plt.ylabel("Numar")
plt.ylim(0, counts.max() + 5)
# plt.show()
plt.savefig("Distributia speciilor.png")

#Histograme
colors = {
    "Iris-setosa": "red",
    "Iris-versicolor": "green",
    "Iris-virginica": "blue"
}
cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

for col in cols:
    plt.figure()
    for label in df['species'].unique():
        df[df['species'] == label][col].plot(kind='hist', alpha=0.58,
            color=colors[label],
            label=label)
    plt.title(f"Histograma pentru {col}")
    plt.xlabel(col)
    plt.ylabel("Frecventa")
    plt.legend()
    plt.savefig(f"Histograma pentru {col}.png")


plt.figure()
Z = linkage(df[cols], method='ward')
dendrogram(Z)
plt.title("Dendograma - Clustering Ierarhic")
plt.savefig("Dendograma - Clustering Ierarhic.png")


k = 3

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[cols])

kmeans = KMeans(n_clusters=k, n_init=10)
kmeans.fit(scaled_data)

df['cluster_kmeans'] = kmeans.labels_

plt.figure()

plt.scatter(
    df['sepal_length'],
    df['sepal_width'],
    c=df['cluster_kmeans'], 
    cmap='viridis',
    s=40
)
centers = scaler.inverse_transform(kmeans.cluster_centers_)
plt.scatter(
    centers[:, 0], centers[:, 1],
    marker='x',
    s=200,
    linewidths=3,
    color='red',
    label='Centroizi'
)
plt.title("Clustere K-Means (sepal_length vs sepal_width)")
plt.xlabel("sepal_length")
plt.ylabel("sepal_width")
plt.legend()
plt.savefig("Clustere K-Means (sepal_length vs sepal_width).png")
plt.figure()

for label in df['species'].unique():
    subset = df[df['species'] == label]
    plt.scatter(subset['sepal_length'], subset['sepal_width'])
plt.title("Clustere reale (sepal_length vs sepal_width)")
plt.xlabel("sepal_length")
plt.ylabel("sepal_width")
plt.legend()
plt.savefig("Clustere reale (sepal_length vs sepal_width).png")
plt.show()
