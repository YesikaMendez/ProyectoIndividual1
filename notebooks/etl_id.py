import ast
import pandas as pd

# Lee el archivo CSV que está en el directorio 'data' dentro de tu proyecto
archivo_csv = '../data/movies_dataset/movies_dataset.csv'
df = pd.read_csv(archivo_csv, low_memory=False)

# Asegurar que las cadenas se conviertan a listas de diccionarios
df['genres'] = df['genres'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Explode la columna 'genres' para que cada fila contenga un solo género
df_exploded = df.explode('genres')

# Filtra filas donde 'genres' es un diccionario válido (no NaN y no vacío)
df_exploded = df_exploded[df_exploded['genres'].apply(lambda x: isinstance(x, dict) and len(x) > 0)]

# Extrae la columna 'id' del DataFrame original, renombrarla a 'movie_id'
df_exploded['movie_id'] = df_exploded['id']

# Convierte cada diccionario en una fila separada
df_genres = pd.json_normalize(df_exploded['genres'])

# Agrega la columna 'movie_id' al DataFrame df_genres
df_genres['movie_id'] = df_exploded['movie_id'].values

# Agrega la columna 'vote_average' al DataFrame df_genres
df_genres['vote_average'] = df_exploded['vote_average'].values

# Muestra el DataFrame resultante
print(df_genres.head())

# guarda el DataFrame en un archivo CSV
output_csv = '../data/movies_dataset/genres_movies.csv'
df_genres.to_csv(output_csv, index=False)

