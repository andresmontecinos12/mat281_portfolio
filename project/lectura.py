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


def elementos_vacios(df,col):
    """
    Entrega información acerca de la cantidad de datos vacios, incluye elementos completados con [].
    parametros:
        df:  dataframe con una serie de columnas
        cols: columna a analizar.
        
    :return: Elementos vacios del dataframe a analizar
    """
    
    
    dato=df[col]
    aux_o=0
    aux_1=0
    if dato.dtype=='O':
        auxp=0
        for j in range(len(dato)):
            if dato.loc[j]=='[]':
                auxp=auxp+1
        aux_o=auxp
        
        #filtro_1=df[col].isnull()
        #aux_o=df[filtro_1][col].shape[0]
        
    else:
        aux_1 = len(dato[dato.isna()])
    
        
        
    #datos vacios completados como string NaN deben ser contados aparte
    return aux_o+aux_1#+aux_3



def elemento_v(df,col):
    dato=df[col]
    aux_o=0
    if dato.dtype=='O':
        #auxp=0
        #for j in range(len(dato)):
        #    if dato.loc[j]=='[]':
        #        auxp=auxp+1
        #aux_o=auxp
        filtro_1=df[col].isnull()
        aux_o=df[filtro_1][col].shape[0]
    return aux_o





    
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
    
    
    # total de elementos 
    l_total = pd_series.count()
    
    # elementos vacios
    l_vacios = elementos_vacios(df,cols)#pd_series[pd_series.isna()]    
    
    # Cantidad de elementos no nulos
    l_nonull =l_total-l_vacios# pd_series.notnull().sum()
    
    # elementos distintos 
    if elemento_v(df,cols)>0:
        l_unique = len(pd_series.unique())-1
    else:
        l_unique=len(pd_series.unique())
     
    l_total_1=l_total
    if l_total<4803:
        l_total=4803
        l_vacios=l_vacios+4803-l_total_1
        l_nonull=l_total-l_vacios
    
    
    
    df_info = pd.DataFrame({
        'Variable': [cols],
        'total_datos':[l_total],
        'total_no_nulos':[l_nonull],
        'unicos': [l_unique],
        'vacios': [l_vacios]
        
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
       

