# Proyecto Individual 1
## Machine Learning Operations (MLOps)

## Descripción del Proyecto

Este proyecto surge como una iniciativa desde el área de Ingeniería de Datos para desarrollar un modelo de

recomendación de machine learning, dirigido a mejorar los servicios de una start-up que provee plataformas 

de streaming. El objetivo principal es solucionar problemas específicos del negocio, optimizando la experiencia 

de los usuarios al recomendarles contenido relevante.

## Objetivo

Para llevar a cabo esta tarea, se emplea un conjunto de datos cuidadosamente seleccionado y procesado mediante

un pipeline de ETL (Extract, Transform, Load), lo que facilita un mejor entendimiento y claridad de los datos. 

Este proceso no solo mejora la calidad de los datos, sino que también incrementa la velocidad y el rendimiento 

del modelo de recomendación que se desarrollará.

## Tabla de contenido 
1. [Introducción](#introducción)
2. [Instalación y Requisitos](#instalación-y-requisitos)
3. [Metodología](#metodología)
4. [Datos y Fuentes](#datos-y-fuentes)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Propósito](#contribución-y-colaboración)
7. [Licencia](#licencia)

## Instalacion y Requisitos 
**Requisitos**
- Python 3.7 o superior
- fastapi
- uvicorn
- scikit-learn
- Pandas
- numpy

**Pasos de instalación**
1. Clonar el repositorio (https://github.com/YesikaMendez/ProyectoIndividual1)
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Instalar las dependencias: `pip install -r requirements.txt`
   
## Metodología

Para llevar a cabo este proyecto, se implementaron diferentes técnicas avanzadas de Ingeniería de Datos, 

como un pipeline de ETL (Extract, Transform, Load) para disponibilizar y limpiar los datos. 

Este proceso incluyó la extracción de datos desde múltiples fuentes, su transformación para eliminar valores nulos, 

normalizar variables y detectar inconsistencias, y la carga final en un formato adecuado para el análisis y el modelado. 

Posteriormente, se realizó un Análisis Exploratorio de Datos (EDA) detallado, donde se aplicaron técnicas como la 

imputación de valores faltantes, la identificación de outliers, y la verificación de la integridad de los datos. 

Este enfoque meticuloso aseguró que los datos utilizados en el modelo de machine learning fueran de alta calidad, 

lo que resultó en un rendimiento óptimo tanto en el modelo como en las consultas de la API. Además, el uso de 

herramientas como pandas para la manipulación de datos y Apache Airflow para la automatización del pipeline de ETL fue

clave para la eficiencia del proyecto."


## Datos y Fuentes
Los datos utilizados en este proyecto provienen del dataset propuestos.

## Estructura del Proyecto

El proyecto se divide en varias secciones clave:

- `data/`: Contiene los archivos de datos utilizados en el proyecto.

- `notebooks/`: Incluye el notebook con el ETL.
Data Preprocessing: Procesamiento y limpieza de los datos a través de múltiples etapas de ETL para asegurar 
su calidad y utilidad
- 
Exploratory Data Analysis (EDA): Realización de un análisis exploratorio de datos para identificar patrones
y tendencias que puedan influir en el modelo de recomendación.

- `src/`: Código fuente del proyecto.
API Development: Desarrollo de una API que expone datos de la empresa a través de 6 funciones clave que 
permiten a otras partes del sistema consumir la información procesada.

Endpoints

/cantidad_filmaciones_mes
/cantidad_filmaciones_dia
/score_titulo
/votos_titulo
/actor
/director

Recommender System: Implementación de un sistema de recomendación donde los usuarios podrán obtener sugerencias
personalizadas de películas, optimizando así la interacción con los servicios de streaming.

Endpoint

/recomendacion

- `README.md`: Archivo de documentación del proyecto.

## Propósito

Este proyecto no solo tiene como objetivo práctico la implementación de un sistema de recomendación eficiente,

sino que también sirve como una plataforma de aprendizaje para aplicar los conocimientos adquiridos en el curso de

'Data Science'.

A través de este proyecto, buscamos demostrar el potencial y la capacidad de generar valor real en el ámbito de la 

Ingeniería de Datos.

## Autores:
Este proyecto fue realizado por: Yesica Mendez
