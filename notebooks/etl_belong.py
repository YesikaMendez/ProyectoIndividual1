import ast
import pandas as pd
from IPython.display import display

# Lee el archivo CSV que está en el directorio 'data' dentro del proyecto
archivo_csv = '../data/movies_dataset.csv'
df = pd.read_csv(archivo_csv, low_memory=False)

# Reemplazar NaN con un diccionario de valores None y convertir cadenas a diccionarios
df['belongs_to_collection'] = df['belongs_to_collection'].apply(
    lambda x: {'id': 0, 'name': "", 'poster_path': "", 'backdrop_path': ""} if pd.isna(x) else ast.literal_eval(x) if isinstance(x, str) else x
)

# Expandir la columna 'belongs_to_collection' en columnas separadas y agregar 'movie_id'
df_belong_to_collection = df['belongs_to_collection'].apply(pd.Series)
df_belong_to_collection['movie_id'] = df['id']

# Filtrar las filas donde 'id' es 0 o NaN
df_belong_to_collection = df_belong_to_collection[df_belong_to_collection['id'].notna() & (df_belong_to_collection['id'] != 0)]

# Convertir 'belong_id' a entero para eliminar '.0'
df_belong_to_collection['id'] = df_belong_to_collection['id'].astype(int)

# Eliminar la columna extra '0' si existe
if 0 in df_belong_to_collection.columns:
    df_belong_to_collection.drop(columns=[0], inplace=True)

# Eliminar las columnas 'poster_path' y 'backdrop_path'
df_belong_to_collection.drop(columns=['poster_path', 'backdrop_path'], inplace=True)

# Renombrar la columna 'id' a 'belong_id'
df_belong_to_collection.rename(columns={'id': 'belong_id'}, inplace=True)

# Guardar el DataFrame resultante en un archivo CSV
output_csv = '../data/belongs_to_collection_clean.csv'
df_belong_to_collection.to_csv(output_csv, index=False)

# Muestra el DataFrame resultante
print(df_belong_to_collection.head())
