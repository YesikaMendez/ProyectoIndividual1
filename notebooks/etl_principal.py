import ast
import pandas as pd
from IPython.display import display

# Lee el archivo CSV que está en el directorio 'data' dentro de tu proyecto
archivo_csv = '../data/movies_dataset.csv'
df = pd.read_csv(archivo_csv, low_memory=False)

# Eliminar las columnas que no serán utilizadas
df = df.drop(columns=['video', 'imdb_id', 'adult', 'poster_path', 'homepage'])

# Convertir 'revenue' y 'budget' a numérico, forzando errores a NaN
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')

# Rellenar valores nulos en 'revenue' y 'budget' con 0
df[['revenue', 'budget']] = df[['revenue', 'budget']].fillna(0)

# Eliminar filas donde 'release_date' es nulo
df = df.dropna(subset=['release_date'])

# Convertir la columna 'release_date' al tipo datetime y formatearla a 'AAAA-mm-dd'
def convert_to_date(date):
    try:
        # Intentar convertir la fecha al formato correcto y luego formatear como 'AAAA-mm-dd'
        date_parsed = pd.to_datetime(date, errors='coerce')
        return date_parsed.strftime('%Y-%m-%d') if date_parsed is not pd.NaT else pd.NaT
    except Exception as e:
        print(f"Error al convertir la fecha: {date}. Error: {e}")
        return pd.NaT

df['release_date'] = df['release_date'].apply(convert_to_date)

# Filtrar filas que no pudieron ser convertidas a una fecha válida
df = df.dropna(subset=['release_date'])

# Convertir 'release_date' de nuevo a datetime para calcular la fecha promedio
df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors='coerce')

# Calcular la fecha promedio, solo si hay fechas válidas
if not df['release_date'].isnull().all():
    mean_date = pd.to_datetime(df['release_date'].mean())
    df['release_date'] = df['release_date'].fillna(mean_date.strftime('%Y-%m-%d'))

# Crear la columna 'release_year' extrayendo el año de 'release_date'
df['release_year'] = df['release_date'].dt.year

# Crear la columna 'return' calculando revenue / budget
df['return'] = df.apply(lambda row: row['revenue'] / row['budget'] if row['budget'] > 0 else 0, axis=1)

# Muestra las primeras filas para verificar los cambios
print(df[['revenue', 'budget', 'return']].head())

# Opcional: guardar el DataFrame en un archivo CSV
output_csv = '../data/principal_movies.csv'
df.to_csv(output_csv, index=False)

