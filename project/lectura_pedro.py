import pandas as pd
import numpy as np

#Descripción de variables de tabla asociadas a archivo 'data/tmdb_5000_movies.csv'


def descripcion_movies(tabla) -> pd.DataFrame:
    
    """
    Breve descripción de la tabla en estudio:
    
    qew: diccionario con definiciones acerca de variables de estudio

    :return: dataframe resumen por columna con información acerca de
            descripción de variables.
    """
    qwe=pd.DataFrame(
    {'Variable':[
        'budget',
        'genres',
        'homepage',
        'id',
        'keywords',
        'original_language',
        'original_title',
        'overview',
        'popularity',
        'production_companies',
        'production_countries',
        'release_date',
        'revenue',
        'runtime',
        'spoken_languages',
        'status',
        'tagline',
        'title',
        'vote_average',
        'vote_count'],
     'Descripción':[
         'El presupuesto en el que se realizó la película.',
         'El género de la película, acción, comedia, suspenso, etc.',
         'Un enlace a la página de inicio de la película.',
         'Es el código de identificación de la película.',
         'Las palabras clave o etiquetas relacionadas con la película.',
         'El idioma en el que se hizo la película.',
         'El título de la película antes de la traducción o adaptación.',
         'Una breve descripción de la película.',
         'Una cantidad numérica que especifica la popularidad de la película.',
         'La casa productora de la película.',
         'El país en el que se produjo.',
         'La fecha en la que se publicó.',
         'Los ingresos mundiales generados por la película.',
         'El tiempo de ejecución de la película en minutos.',
         'Otros idiomas en que se escucha la pelicula',
         '"Liberado" o "Rumoreado".',
         'Eslogan de la película.',
         'título de la película.',
         'Calificaciones promedio que recibió la película.',
         'El recuento de votos recibidos.']})
    
    qwe2=pd.DataFrame({
        'Variable':[
            'id',
            'cast',
            'crew'],
        'Descripción':[
            'Idenfificador único de la película',
            'Conjunto de actores',
            'El nombre del director, editor, compositor, escritor, etc.']
    })


    
    
    if tabla==1:
        return qwe2
    elif tabla==2:
        return qwe
    else:
        ""


    
def tabla_descripcion(df,descrip) -> pd.DataFrame:
    """
    Resumir la información disponible en tabla
    parametros:
        df:  dataframe con una serie de columnas
        descrip:información acerca del significado de cada columna
        
    :return: dataframe resumen por columna con información acerca de
             descripción y tipo de dato por columna.
    """
    
    tabla_resumen1=pd.DataFrame({'Variable':df.columns,'Tipo de Dato':df.dtypes})
    tabla_resumen1=tabla_resumen1.merge(descrip,on='Variable')
    
    return tabla_resumen1



    
def resumen_columna(df,cols):
    """
    Entrega información acerca de la cantidad de datos de columna especifica.
    parametros:
        df:  dataframe con una serie de columnas
        cols: columna a analizar.
        
    :return: resumen por columna con información acerca de
             total de elementos, elemento no nulos, elementos nulos, distintos y vacios
    """
    
    
    pd_series = df[cols]
    
    #for j in range(len(pd_series)):
    #    if pd_series.loc[j]==[]:
    #        pd_series.loc[j]=np.nan

    
    
    
    # total de elementos 
    l_total = pd_series.count()
    
    
    
    
    
    # Cantidad de elementos no nulos
    l_nonull = pd_series.notnull().sum()
    
    # elementos distintos 
    l_unique = pd_series.unique()
 
    # elementos vacios
    l_vacios = pd_series[pd_series.isna()]
    
    df_info = pd.DataFrame({
        'Variable': [cols],
        'total_datos':[l_total],
        'unicos': [len(l_unique)],
        'vacios': [len(l_vacios)]
        
    })
    
    return df_info
    
    
def resumen_por_columnas(df):
    """
    Entrega información acerca de las columnas de un dataframe.
    parametros:
        df:  dataframe con una serie de columnas

        
    :return: resumen por columna con información acerca de tipo de dato, descripcion, 
             total de elementos, elementos unicos y vacios.
    """
    frames = []
    for col in df.columns:
        aux_df = resumen_columna(df,col)
        frames.append(aux_df)
    
    df_info = pd.concat(frames).reset_index(drop=True)
    df_info
    
    return df_info
       

def get_list(x):
    """
    Entrega los primeros 4 elementos o todos los elementos de una columna dataframe en el caso que la cadena tenga menos de 4 elementos.
    parametros:
        x:  dataframe columna.

        
    :return: lista de 4 elementos o menos.
    """    
    
    
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 4:
            names = names[:4]
        return names

    #Return empty list in case of missing/malformed data
    return []




def redondear(a,decimal):
    
    """
    Entrega la decada a la que pertenece cierto año. 
    parametros:
        a:  dataframe columna.
        decimal: Por default este valor debiese ser -1, para decada. Puede usarse otro valor para considerar siglos o milenios pero debe
        modificar el código siguiente.

        
    :return: lista con las decadas asociada a cierto dataframe de entrada (columna de tipo numérico).
    """   
    
    
    lista=[]
    for i in a:
        if i< round(i,decimal):
            b=round(i,decimal)-10
        else:
            b=round(i,decimal)
        lista.append(b)
    return lista

def descomponer(a):
    """
    Entrega primer elemento de una cadena dentro de un dataframe.
    parametros:
        a:  dataframe columna.
        
    :return: primer elemento de una cadena.
    """   
    lista=[]
    for i in range(0,len(a)):
        if len(a['genres'][i])==0:
            lista.append('NaN')
        else:
            lista.append(a['genres'][i][0])
        
    return lista

def filtro_demografico(x,col,genero,cantidad):
    """
    Entrega un dataframe con una cantidad sugerida modificable
    
        x:        dataframe con la información
        col:      columna para filtrar el dataframe (EJ: Género)
        genero:   valor que filtra el data frame    (Ej: 'Comedy')
        cantidad: Cantidad de datos sugeridos que solicite 

    :return: dataframe con las películas sugeridas.
    """
    mask=x[col]==genero
    x=x[mask]
    v=x['vote_count']
    R=x['vote_average']
    C= x['vote_average'].mean()
    m= x['vote_count'].quantile(0.9)
    score=(v/(v+m) * R) + (m/(m+v) * C)
    q_movies = x.copy().loc[x['vote_count'] >= m]
    q_movies['score'] = score 
    q_movies = q_movies.sort_values('score', ascending=False)
    
    return q_movies[['title', 'vote_count', 'vote_average', 'score']].head(cantidad)

