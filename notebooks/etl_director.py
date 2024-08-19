import ast
import pandas as pd
import unicodedata


def normalizar_texto(texto):
    # Verificar si el texto es una cadena
    if isinstance(texto, str):
        # Eliminar tildes y convertir a minúsculas
        texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8').lower()
        return texto_normalizado
    else:
        return texto  # Si no es una cadena, devolver el valor tal cual


# Cargar el DataFrame de los actores
archivo_csv_cast = '../data/credits/credits.csv'
df_cast = pd.read_csv(archivo_csv_cast, low_memory=False)

# Cargar el DataFrame de las películas con budget y revenue
archivo_csv_movie = '../data/movies_dataset/principal_movies.csv'
df_movie = pd.read_csv(archivo_csv_movie, low_memory=False)

# Convertir la columna 'id' a números, valores no convertibles se convierten a NaN
df_movie['id'] = pd.to_numeric(df_movie['id'], errors='coerce')

# Filtrar las filas donde 'id' es NaN
df_movie = df_movie.dropna(subset=['id'])

# Convertir la columna 'id' a entero después de eliminar los NaN
df_movie['id'] = df_movie['id'].astype(int)

# Continuar con el resto del proceso
# Convertir la columna 'cast' de string a lista de diccionarios si es necesario
df_cast['crew'] = df_cast['crew'].apply(ast.literal_eval)

# Usar explode para credito en una fila distinta
df_crew_exploded = df_cast.explode('crew').reset_index(drop=True)

# Desanidar solo los campos 'name' y 'id' del diccionario
df_cast_final = pd.json_normalize(df_crew_exploded['crew'])[['name', 'job']]

#renombrar campo id
df_cast_final['movie_id'] = df_crew_exploded['id'].values

# Asegurarse de que ambas columnas 'movie_id' y 'id' tengan el mismo tipo de dato
df_cast_final['movie_id'] = df_cast_final['movie_id'].astype(int)

# Filtrar el cargo de director
df_cast_final = df_cast_final[df_cast_final['job'] == 'Director'].reset_index(drop=True)

# Realizar la unión de df_cast_final con df_movie usando el campo 'id'
df_merged = pd.merge(df_cast_final, df_movie[['id', 'budget', 'revenue', 'original_title', 'release_year', 'return']], left_on='movie_id', right_on='id')

# Eliminar la columna 'id' que proviene de df_movie si no la necesitas
df_merged.drop(columns=['id'], inplace=True)

# Reemplazar NaN en la columna 'name' por una cadena vacía antes de aplicar la normalización
df_merged['name'] = df_merged['name'].fillna('').apply(normalizar_texto)

# Reorganizar las columnas para que quede el id de la película, el nombre del actor, el presupuesto, la recaudación y el retorno
df_merged = df_merged[['movie_id', 'original_title', 'name', 'budget', 'revenue', 'release_year', 'return']]

#Ganancis obtenidas
df_merged['ganancia'] = df_merged['revenue'] - df_merged['budget']

# Opcional: guardar el DataFrame en un archivo CSV
output_csv = '../data/credits/director.csv'
df_merged.to_csv(output_csv, index=False)
