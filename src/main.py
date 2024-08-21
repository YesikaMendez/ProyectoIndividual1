import ast
import numpy as np
import unicodedata
from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

dias_semana = {
    'Monday': 'Lunes',
    'Tuesday': 'martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}
app = FastAPI()


def normalizar_texto(texto):
    # Eliminar tildes y convertir a minúsculas
    texto_normalizado = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8').lower()
    return texto_normalizado


# load data genres
df_genres = pd.read_csv('data/movies_dataset/genres_movies.csv', names=['id', 'name', 'movie_id', 'vote_average'])

# Convert movie_id to int
df_genres['movie_id'] = pd.to_numeric(df_genres['movie_id'], errors='coerce').fillna(0).astype(int)

# Group the genres by movie_id and create a list of genres for each movie
grouped = df_genres.groupby('movie_id')['name'].apply(list).reset_index()

# Create a DataFrame movie genres group
movies_df_genres = pd.DataFrame(grouped)

# Unique genres
unique_genres = list(set(genre for genres in movies_df_genres['name'] for genre in genres))


# Function to convert genres to vectors
def genres_to_vector(genres):
    return np.array([1 if genre in genres else 0 for genre in unique_genres])


# Convert all movie genres to vectors and add to DataFrame
movies_df_genres['vector'] = movies_df_genres['name'].apply(genres_to_vector)


@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: int):
    archivo_csv = 'data/movies_dataset/principal_movies.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    # Convertir la columna 'release_date' a datetime para facilitar la extracción del mes
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Filtrar las filmaciones por el mes
    filmaciones_mes = df[df['release_date'].dt.month == mes]

    # Contar la cantidad de filmaciones
    cantidad = filmaciones_mes.shape[0]

    return {"mes": mes, "cantidad_filmaciones": cantidad}


@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    archivo_csv = 'data/movies_dataset/principal_movies.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    # Convertir la columna 'release_date' a datetime para facilitar la extracción del día de la semana
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Extraer el día de la semana en inglés
    df['dia_semana'] = df['release_date'].dt.day_name()

    # Convertir el día de la semana a español y normalizar
    df['dia_semana_es'] = df['dia_semana'].map(dias_semana)
    df['dia_semana_es_normalizado'] = df['dia_semana_es'].apply(normalizar_texto)

    # Normalizar la entrada del usuario
    dia_normalizado = normalizar_texto(dia)

    # Filtrar las filmaciones por el día en español normalizado
    filmaciones_dia = df[df['dia_semana_es_normalizado'] == dia_normalizado]

    # Contar la cantidad de filmaciones en ese día
    cantidad = filmaciones_dia.shape[0]

    return {"dia": dia, "cantidad_filmaciones": cantidad}


@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    archivo_csv = 'data/movies_dataset/principal_movies.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    #Normalizar texto
    df['original_title_normalizado'] = df['original_title'].apply(normalizar_texto)

    #Normalizar texto de entrada
    titulo_de_la_filmacion_normalizado = normalizar_texto(titulo_de_la_filmacion)

    # Filtrar el DataFrame por el título
    df_filtrado = df[df['original_title'].str.contains(titulo_de_la_filmacion_normalizado, case=False, na=False)]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Filmación no encontrada")

    # Obtener el título, año y score
    titulo = df_filtrado.iloc[0]['original_title']
    year = int(df_filtrado.iloc[0]['release_year']) if pd.notna(df_filtrado.iloc[0]['release_year']) else None
    score = float(df_filtrado.iloc[0]['vote_average']) if pd.notna(df_filtrado.iloc[0]['vote_average']) else None

    return {"titulo": titulo, "año": year, "score": score}


@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    archivo_csv = 'data/movies_dataset/principal_movies.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    #Normalizar texto
    df['original_title_normalizado'] = df['original_title'].apply(normalizar_texto)

    #Normalizar texto de entrada
    titulo_de_la_filmacion_normalizado = normalizar_texto(titulo_de_la_filmacion)

    # Filtrar el DataFrame por el título
    df_filtrado = df[
        df['original_title_normalizado'].str.contains(titulo_de_la_filmacion_normalizado, case=False, na=False)]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Filmación no encontrada")

    # Verificar si el número de votos es menor a 2000
    if df_filtrado.iloc[0]['vote_count'] < 2000:
        raise HTTPException(status_code=400,
                            detail="La filmación no cumple con el criterio de votos (menos de 2000 votos)")

    # Obtener el título, año y score
    titulo = df_filtrado.iloc[0]['original_title']
    year = int(df_filtrado.iloc[0]['release_year']) if pd.notna(df_filtrado.iloc[0]['release_year']) else None
    votos = int(df_filtrado.iloc[0]['vote_count']) if pd.notna(df_filtrado.iloc[0]['vote_count']) else None
    score = float(df_filtrado.iloc[0]['vote_average']) if pd.notna(df_filtrado.iloc[0]['vote_average']) else None

    return {"titulo": titulo, "año": year, "votos": votos, "score": score}


@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    archivo_csv = 'data/credits/actor.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    #Normalizar texto de entrada
    nombre_actor_normalizado = normalizar_texto(nombre_actor)

    # Filtrar el DataFrame por el título
    df_filtrado = df[df['name'].str.contains(nombre_actor_normalizado, case=False, na=False)]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")

    # Calcular el éxito del actor sumando los retornos
    exito_total = df_filtrado['return'].sum()

    # Contar el número de películas
    cantidad_peliculas = df_filtrado['movie_id'].nunique()

    # Calcular el promedio de retorno
    promedio_retorno = exito_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return {
        "actor": nombre_actor,
        "exito_total": exito_total,
        "cantidad_peliculas": cantidad_peliculas,
        "promedio_retorno": promedio_retorno
    }


@app.get("/director/{nombre_director}")
def get_director(nombre_director: str):
    archivo_csv = 'data/credits/director.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    # Normalizar texto de entrada
    nombre_director_normalizado = normalizar_texto(nombre_director)

    # Filtrar el DataFrame por el título
    df_filtrado = df[df['name'].str.contains(nombre_director_normalizado, case=False, na=False)]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado en el dataset")

    # Calcular el éxito total del director (suma de retornos)
    exito_total = df_filtrado['return'].sum()

    # Preparar la lista de películas con la información solicitada
    peliculas = df_filtrado[['original_title', 'release_year', 'return', 'budget', 'revenue', 'ganancia']].to_dict(
        orient='records')

    # Construir la respuesta
    respuesta = {
        "director": nombre_director,
        "exito_total": exito_total,
        "peliculas": peliculas
    }

    return respuesta

@app.get("/")
def read_root():
    return {"Hello": "Soy Henry"}

@app.get("/recomendacion/{titulo_de_la_filmacion}")
def get_recomendacion(titulo_de_la_filmacion: str):
    archivo_csv = 'data/movies_dataset/principal_movies.csv'
    df = pd.read_csv(archivo_csv, low_memory=False)

    # Normalizar texto
    df['original_title_normalizado'] = df['original_title'].apply(normalizar_texto)

    # Normalizar texto de entrada
    titulo_de_la_filmacion_normalizado = normalizar_texto(titulo_de_la_filmacion)

    # Filtrar el DataFrame por el título
    df_filtrado = df[df['original_title_normalizado'].str.contains(titulo_de_la_filmacion_normalizado, case=False, na=False)]

    if df_filtrado.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada para dar recomendaciones")

    # Recuperar el movie_id del primer resultado
    movie_id = df_filtrado.iloc[0]['id']

    if movie_id not in movies_df_genres['movie_id'].values:
        print(f"Movie ID {movie_id} not found. Available movie IDs: {movies_df_genres['movie_id'].unique()}")
        return []

    # Obtén el vector del género de la película objetivo
    movie_genre_vector = movies_df_genres.loc[movies_df_genres['movie_id'] == movie_id, 'vector'].values[0].reshape(1, -1)

    # Calcular las similitudes de forma vectorizada
    all_vectors = np.vstack(movies_df_genres['vector'].values)
    similarities = cosine_similarity(movie_genre_vector, all_vectors)[0]

    # Asignar las similitudes a los movie_id correspondientes
    movies_df_genres['similarity'] = similarities

    # generar data frame para peso de vote average
    movies_df_genres_votes = movies_df_genres.merge(df[['id', 'vote_average']], left_on='movie_id', right_on='id', how='left')

    # Normalizar vote_average
    max_vote = movies_df_genres_votes['vote_average'].max()
    min_vote = movies_df_genres_votes['vote_average'].min()
    movies_df_genres_votes['vote_average_normalized'] = (movies_df_genres_votes['vote_average'] - min_vote) / (max_vote - min_vote)

    # Combinar similitud con vote_average
    movies_df_genres['combined_score'] = movies_df_genres['similarity'] * 0.6 + movies_df_genres_votes[
        'vote_average_normalized'] * 0.4

    # Filtrar las 5 películas con mayor puntaje combinado
    top_movies = movies_df_genres[movies_df_genres['movie_id'] != movie_id].nlargest(5, 'combined_score')

    # Obtener los títulos de las películas recomendadas
    recommended_titles = df[df['id'].isin(top_movies['movie_id'])][['original_title']].to_dict(
        orient='records')

    respuesta = {
        "recomendaciones": recommended_titles,
    }

    return respuesta




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
