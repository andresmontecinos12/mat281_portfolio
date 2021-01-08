#hacer la mejor predicción de cada imagen. Para ellos es necesario realizar los pasos clásicos de un proyecto de _Machine Learning_, como #
#estadística descriptiva, visualización y preprocesamiento.




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
        