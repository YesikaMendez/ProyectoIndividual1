import ast
import pandas as pd
from IPython.display import display

# Lee el archivo CSV que está en el directorio 'data' dentro de tu proyecto
archivo_csv = '../data/movies_dataset.csv'
df = pd.read_csv(archivo_csv, low_memory=False)

# Asegurarse de que las cadenas se conviertan a listas de diccionarios
df['genres'] = df['genres'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Explode la columna 'genres' para que cada fila contenga un solo género
df_exploded = df.explode('genres')

# Filtrar filas donde 'genres' es un diccionario válido (no NaN y no vacío)
df_exploded = df_exploded[df_exploded['genres'].apply(lambda x: isinstance(x, dict) and len(x) > 0)]


# Convertir cada diccionario en una fila separada
df_genres = pd.json_normalize(df_exploded['genres'])

# Eliminar duplicados basados en las columnas 'id' y 'name'
df_genres = df_genres.drop_duplicates(subset=['id', 'name'])

# Resetear el índice para un DataFrame limpio
df_genres.reset_index(drop=True, inplace=True)

# Muestra el DataFrame resultante
print(df_genres.head())

# Opcional: guardar el DataFrame en un archivo CSV
output_csv = '../data/genres_unique.csv'
df_genres.to_csv(output_csv, index=False)
