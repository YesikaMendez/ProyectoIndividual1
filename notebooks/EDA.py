import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Lee el archivo CSV que está en el directorio 'data' dentro de tu proyecto
archivo_principal = '../data/movies_dataset/principal_movies.csv'
df_movies = pd.read_csv(archivo_principal, low_memory=False)

archivo_generos = '../data/movies_dataset/genres_movies.csv'
df_genres = pd.read_csv(archivo_generos, low_memory=False)

# Convertir las columnas 'id' y 'movie_id' al mismo tipo de dato
df_movies['id'] = df_movies['id'].astype(str)
df_genres['movie_id'] = df_genres['movie_id'].astype(str)

# Mostrar las primeras filas del dataset de películas
print("Primeras filas del dataset de películas:")
print(df_movies.head())

# Mostrar las primeras filas del dataset de géneros
print("\nPrimeras filas del dataset de géneros:")
print(df_genres.head())

# Información general del dataset de películas
print("\nInformación del dataset de películas:")
print(df_movies.info())

# Información general del dataset de géneros
print("\nInformación del dataset de géneros:")
print(df_genres.info())

# Resumen estadístico de las columnas numéricas del dataset de películas
print("\nResumen estadístico de las columnas numéricas del dataset de películas:")
print(df_movies.describe())

# Verificar valores nulos en el dataset de películas
print("\nValores nulos en cada columna del dataset de películas:")
print(df_movies.isnull().sum())

# Imputación de valores nulos en el dataset de películas
df_movies['belongs_to_collection'] = df_movies['belongs_to_collection'].fillna('No Collection')
df_movies['original_language'] = df_movies['original_language'].fillna(df_movies['original_language'].mode()[0])
df_movies['overview'] = df_movies['overview'].fillna('Sin Descripción')
df_movies['runtime'] = df_movies['runtime'].fillna(df_movies['runtime'].median())
df_movies['status'] = df_movies['status'].fillna(df_movies['status'].mode()[0])
df_movies['tagline'] = df_movies['tagline'].fillna('Sin Tagline')

# Reemplazar valores 0 en 'budget' y 'revenue' con NaN para tratamiento posterior
df_movies['budget'] = df_movies['budget'].replace(0, pd.NA)
df_movies['revenue'] = df_movies['revenue'].replace(0, pd.NA)

# Manejo de outliers: visualización de boxplots para budget y revenue
plt.figure(figsize=(10, 6))
sns.boxplot(x=df_movies['budget'])
plt.title('Boxplot de Budget')
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x=df_movies['revenue'])
plt.title('Boxplot de Revenue')
plt.show()

# Imputación de valores faltantes en 'budget' y 'revenue' con la mediana
df_movies['budget'] = df_movies['budget'].fillna(df_movies['budget'].median()).infer_objects(copy=False)
df_movies['revenue'] = df_movies['revenue'].fillna(df_movies['revenue'].median()).infer_objects(copy=False)

# Unir el dataset de películas con el dataset de géneros
df_combined = pd.merge(df_movies, df_genres, left_on='id', right_on='movie_id')

# Filtrar solo las columnas numéricas para el cálculo de la correlación
numeric_columns = df_combined.select_dtypes(include=['number'])

# Verificar si hay columnas que no pueden convertirse a float y excluirlas
for col in numeric_columns.columns:
    try:
        numeric_columns[col].astype(float)
    except ValueError:
        print(f"Columna '{col}' contiene valores que no pueden convertirse a float y será excluida.")
        numeric_columns = numeric_columns.drop(columns=[col])

# Calcular la correlación entre las variables numéricas
correlation_matrix = numeric_columns.corr()

# Mostrar el heatmap de la correlación
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Heatmap de Correlación entre Variables Numéricas')
plt.show()

# Visualización de la distribución de las columnas numéricas en el dataset combinado
print("\nDistribución de las columnas numéricas en el dataset combinado:")
df_combined[numeric_columns.columns].hist(bins=50, figsize=(20, 15))
plt.show()

# Conteo de los géneros más frecuentes en el dataset combinado
print("\nDistribución de géneros en el dataset combinado:")
plt.figure(figsize=(10, 6))
sns.countplot(y='name', data=df_combined, order=df_combined['name'].value_counts().index)
plt.title('Distribución de Géneros')
plt.show()

# Relación entre la calificación (vote_average) y el año de lanzamiento (release_year)
print("\nRelación entre calificación y año de lanzamiento en el dataset combinado:")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='release_year', y='vote_average', data=df_combined)
plt.title('Relación entre Calificación y Año de Lanzamiento')
plt.show()

# Boxplot de la calificación por género en el dataset combinado
print("\nBoxplot de la calificación por género en el dataset combinado:")
plt.figure(figsize=(12, 8))
sns.boxplot(x='name', y='vote_average', data=df_combined)
plt.xticks(rotation=45)
plt.title('Boxplot de Calificación por Género')
plt.show()

# Análisis de outliers en la calificación (vote_average) en el dataset combinado
print("\nAnálisis de outliers en la calificación en el dataset combinado:")
plt.figure(figsize=(10, 6))
sns.boxplot(df_combined['vote_average'])
plt.title('Boxplot de Calificación (Vote Average)')
plt.show()

# Histograma de las películas más exitosas (revenue y vote_average altos)
print("\nHistograma de las Películas Más Exitosas:")
plt.figure(figsize=(12, 8))
top_movies = df_combined[(df_combined['revenue'] > df_combined['revenue'].quantile(0.75)) &
                         (df_combined['vote_average'] > df_combined['vote_average'].quantile(0.75))]
sns.histplot(top_movies['revenue'], bins=20, kde=True)
plt.title('Distribución de Revenue en las Películas Más Exitosas')
plt.xlabel('Revenue')
plt.ylabel('Número de Películas')
plt.show()
