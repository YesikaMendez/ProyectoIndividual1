import pandas as pd
import matplotlib.pyplot as plt

# Lee el archivo CSV que está en el directorio 'data' dentro de tu proyecto
archivo_principal = '../data/movies_dataset/principal_movies.csv'
df_movies = pd.read_csv(archivo_principal, low_memory=False)

archivo_generos = '../data/movies_dataset/genres_movies.csv'
df_genres = pd.read_csv(archivo_generos, low_memory=False)

# Convierte las columnas 'id' y 'movie_id' al mismo tipo de dato
df_movies['id'] = df_movies['id'].astype(int)


# Muestra las primeras filas del dataset de películas
print("Primeras filas del dataset de películas:")
print(df_movies.head())

# Información general del dataset de películas
print("\nInformación del dataset de películas:")
print(df_movies.info())

# Resumen estadístico de las columnas numéricas del dataset de películas
print("\nResumen estadístico de las columnas numéricas del dataset de películas:")
print(df_movies.describe())

# Verifica valores nulos en el dataset de películas
print("\nValores nulos en cada columna del dataset de películas:")
print(df_movies.isnull().sum())

# Imputación de valores nulos en el dataset de películas
df_movies['belongs_to_collection'] = df_movies['belongs_to_collection'].fillna('No Collection')
df_movies['original_language'] = df_movies['original_language'].fillna(df_movies['original_language'].mode()[0])
df_movies['overview'] = df_movies['overview'].fillna('Sin Descripción')
df_movies['runtime'] = df_movies['runtime'].fillna(df_movies['runtime'].median())
df_movies['status'] = df_movies['status'].fillna(df_movies['status'].mode()[0])
df_movies['tagline'] = df_movies['tagline'].fillna('Sin Tagline')

# Reemplaza valores 0 en 'budget' y 'revenue' con NaN para tratamiento posterior
df_movies['budget'] = df_movies['budget'].replace(0, pd.NA)
df_movies['revenue'] = df_movies['revenue'].replace(0, pd.NA)

# Imputación de valores faltantes en 'budget' y 'revenue' con la mediana
df_movies['budget'] = df_movies['budget'].fillna(df_movies['budget'].median())
df_movies['revenue'] = df_movies['revenue'].fillna(df_movies['revenue'].median())

# Descripción estadística de las columnas relevantes
print(df_movies[['vote_average', 'revenue', 'budget']].describe())

# Histograma de la columna vote_average
plt.figure(figsize=(10, 6))
plt.hist(df_movies['vote_average'].dropna(), bins=20, edgecolor='k', alpha=0.7)
plt.title('Distribución de Vote Average')
plt.xlabel('Vote Average')
plt.ylabel('Frecuencia')
plt.grid(True)

# Guarda el gráfico como un archivo PNG
plt.savefig('histograma_vote_average.png')
plt.close()

# Cuenta la cantidad de películas por cada género
genre_counts = df_genres['name'].value_counts().head(10)

# Crea el histograma
plt.figure(figsize=(12, 8))
genre_counts.plot(kind='bar', edgecolor='k', alpha=0.7)
plt.title('Cantidad de Películas por Género')
plt.xlabel('Género')
plt.ylabel('Cantidad de Películas')
plt.xticks(rotation=45)
plt.grid(True)

# Guarda el gráfico como un archivo PNG
plt.savefig('histograma_genres.png')
plt.close()