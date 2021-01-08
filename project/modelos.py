
#### librerías
import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
    
from sklearn.model_selection import train_test_split
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
from sklearn.metrics import mean_squared_error

from metrics_regression import *


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



def filtro_basado_contenido(title,df2,num):    
    tfidf = TfidfVectorizer(stop_words='english')
    df2['overview'] = df2['overview'].fillna('')
    df4=df2
    tfidf_matrix = tfidf.fit_transform(df4['overview'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df4.index, index=df4['title']).drop_duplicates()
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num+1]
    movie_indices = [i[0] for i in sim_scores]

    return df4['title'].iloc[movie_indices]




def get_mse(preds, actuals):
    if preds.shape[1] != actuals.shape[1]:
        actuals = actuals.T
    preds = preds[actuals.nonzero()].flatten()
    actuals = actuals[actuals.nonzero()].flatten()
    return mean_squared_error(preds, actuals)
 




def filtro_colaborativo_usuario(df_matrix,pr,user_id1,topx):
    ratings = df_matrix.values
    ratings_train, ratings_test = train_test_split(ratings, test_size = 0.2, random_state=42)
    sim_matrix = 1 -cosine_distances(ratings)
    #separar las filas y columnas de train y test
    sim_matrix_train = sim_matrix[0:536,0:536]
    sim_matrix_test = sim_matrix[536:670,536:670]
    #Predicciones
    users_predictions = sim_matrix_train.dot(ratings_train) / np.array([np.abs(sim_matrix_train).sum(axis=1)]).T
    
    #
    data = pr[pr['user_id'] == user_id1]
    usuario_ver = data.iloc[0]['user_id'] - 1 #resta 1 para el index panda
    user0=users_predictions.argsort()[usuario_ver]   #ordenar indices de menor a mayor de las peliculas proyectadas
    # Veamos los 10 recomendados con mayor puntaje en la predic para este usuario
    ta=pd.DataFrame({'film':df_matrix.columns[user0[-topx:]],'puntaje':users_predictions[usuario_ver][user0[-topx:]]})
    tabla_recomendacion=ta.sort_values('puntaje',ascending=False)[['film','puntaje']]
 
    
    # Realizo las predicciones para el test set
    users_predictions_test = sim_matrix.dot(ratings) / np.array([np.abs(sim_matrix).sum(axis=1)]).T
    users_predictions_test = users_predictions_test[536:670,:]
    error_entrenamiento=get_mse(users_predictions, ratings_train)
    error_prueba=get_mse(users_predictions_test, ratings_test)
    
    entrenamiento=pd.DataFrame({'y':ratings_train[ratings_train.nonzero()].flatten(),'yhat':users_predictions[ratings_train.nonzero()].flatten()})
    
    prueba=pd.DataFrame({'y':ratings_test[ratings_test.nonzero()].flatten(),'yhat':users_predictions_test[ratings_test.nonzero()].flatten()})


    df_metrics_entrenamiento = summary_metrics(entrenamiento)
    df_metrics_entrenamiento['etapa']='entrenamiento'
    df_metrics_prueba=summary_metrics(prueba)
    df_metrics_prueba['etapa']='prueba'
    resumen=pd.concat([df_metrics_entrenamiento, df_metrics_prueba])
    
    return tabla_recomendacion,sim_matrix,error_entrenamiento,error_prueba,resumen


def filtro_colaborativo_item(df_matrix,pr,user_id1,peli,topx):
    ratings = df_matrix.values
    ratings_train_item, ratings_test_item = train_test_split(ratings.T, test_size = 0.2, shuffle=False, random_state=42)
    sim_matrix_item=1 -cosine_distances(ratings.T)
    #separar las filas y columnas de train y test
    sim_matrix_train_item = sim_matrix_item[0:684,0:684]
    sim_matrix_test_item = sim_matrix_item[684:856,684:856]
    #Predicciones
    item_predictions = sim_matrix_train_item.dot(ratings_train_item) / np.array([np.abs(sim_matrix_train_item).sum(axis=1)]).T
    
    prwewd=df_matrix.T[[1][0]]
    lista_peli=pd.DataFrame({'Film':[x for x in prwewd.index]})
    
    
    data = pr[pr['user_id'] == user_id1]
    usuario_ver = data.iloc[0]['user_id'] - 1 #resta 1 para el index panda
    
    ###----------------------------------
    
    PELICULA_EJEMPLO = peli
    data_item = pr[pr['original_title'] == PELICULA_EJEMPLO]
    #item_ver = data_item.iloc[0]['id'] - 1 # resta 1 para obtener el index de pandas.
    #data_item
    item_ver=lista_peli[lista_peli['Film']==PELICULA_EJEMPLO].index.tolist()[0]

    
    
    #item_predictions[:][usuario_ver]
    item0_mejor_evaluado=item_predictions.argsort(axis=0)[:,usuario_ver]
    #item0_mejor_evaluado

    #df_matrix.columns[item0_mejor_evaluado]
    # Veamos los 10 recomendados con mayor puntaje en la predic para este usuario


    ta1_film=pd.DataFrame({'film':df_matrix.columns[item0_mejor_evaluado],'puntaje':item_predictions[item0_mejor_evaluado][:,usuario_ver]})
    tabla_recomendacion1_film=ta1_film.sort_values('puntaje',ascending=False)[['film','puntaje']]
    
    
    # Realizo las predicciones para el test set
    item_predictions_test = sim_matrix_item.dot(ratings.T) / np.array([np.abs(sim_matrix_item).sum(axis=1)]).T
    item_predictions_test = item_predictions_test[684:856,:]
    entrenamiento=pd.DataFrame({'y':ratings_train_item[ratings_train_item.nonzero()].flatten(),'yhat':item_predictions[ratings_train_item.nonzero()].flatten()})
    
    prueba=pd.DataFrame({'y':ratings_test_item[ratings_test_item.nonzero()].flatten(),'yhat':item_predictions_test[ratings_test_item.nonzero()].flatten()})
    
    
    df_metrics_entrenamiento = summary_metrics(entrenamiento)
    df_metrics_entrenamiento['etapa']='entrenamiento'
    df_metrics_prueba=summary_metrics(prueba)
    df_metrics_prueba['etapa']='prueba'
    ads=pd.concat([df_metrics_entrenamiento, df_metrics_prueba])


    
    
    
   
    
    return tabla_recomendacion1_film,ads

    

    