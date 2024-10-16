import pandas as pd
from fuzzywuzzy import fuzz

# Cargar los datos
df_reales = pd.read_csv("./data/DatosReales_15_10_2024.csv")
df_fifa = pd.read_csv("./data/players_22.csv")

# Preprocesamiento
df_reales.drop(columns=["Unnamed: 0"], inplace=True)
df_reales = df_reales[df_reales["goles"] > 0]
df_reales.reset_index(drop=True, inplace=True)

# Filtrar las columnas necesarias del dataframe FIFA
df_fifa = df_fifa[df_fifa["league_name"].isin(["Italian Serie A", "French Ligue 2","English Premier League","Spain Primera Division","German 1. Bundesliga"])]
df_fifa = df_fifa[["sofifa_id", "short_name", "long_name"]]

# Inicializar la columna 'match_id' si no existe
if "match_id" not in df_reales.columns:
    df_reales["match_id"] = 0  # Crear la columna y llenarla inicialmente con 0

# Función de matching
def matchear_con_columna(df_reales, df_fifa, threshold=80):
    # Convertir columnas en listas para optimizar el acceso
    nombres_goleadores = df_reales["nombre"].tolist()
    nombres_fifa_long = df_fifa["long_name"].tolist()
    nombres_fifa_short = df_fifa["short_name"].tolist()
    lista_a_matchear = df_fifa["sofifa_id"].tolist()

    # Recorrer los nombres de los goleadores
    for i, goleador in enumerate(nombres_goleadores):
        match_found = False  # Bandera para verificar si se encontró un match
        print(i,goleador)

        # Comprobación exacta o fuzzy con nombres largos
        for j, fifa_long in enumerate(nombres_fifa_long):
            print(j,fifa_long)
            if goleador == fifa_long:
                df_reales.at[i, "match_id"] = lista_a_matchear[j]
                match_found = True
                break
            else:
                if " " in goleador:
                    elemento_fuzzi = goleador.split(" ")[1]
                else:
                    elemento_fuzzi = goleador
                ratio = fuzz.token_sort_ratio(elemento_fuzzi, fifa_long)
                if ratio >= threshold:
                    df_reales.at[i, "match_id"] = lista_a_matchear[j]
                    match_found = True
                    break

        # Si no se encontró match con nombres largos, se comprueba con nombres cortos
        if not match_found:
            for j, fifa_short in enumerate(nombres_fifa_short):
                print(j,fifa_short)
                if goleador == fifa_short:
                    df_reales.at[i, "match_id"] = lista_a_matchear[j]
                    match_found = True
                    break
                else:
                    ratio = fuzz.token_sort_ratio(goleador, fifa_short)
                    if ratio >= threshold:
                        df_reales.at[i, "match_id"] = lista_a_matchear[j]
                        match_found = True
                        break

        # Si no se encontró ningún match, asignar 0
        if not match_found:
            df_reales.at[i, "match_id"] = 0

    return df_reales, df_fifa

# Ejecutar el proceso de matching
df_reales, df_fifa = matchear_con_columna(df_reales, df_fifa)


# Resultados
print("DataFrame Reales Actualizado:")
print(df_reales)

            
df_reales.to_csv("goleadores_reales_id.csv")
print("FIN")
print("FIN")


"""
#------------------------------------------
import pandas as pd
from fuzzywuzzy import fuzz


df_reales = pd.read_csv("./data/DatosReales_15_10_2024.csv")
df_fifa = pd.read_csv("./data/players_22.csv")

def crear_id_merge(df_reales,df_fifa):

    # Asegúrate de que la columna 'match_id' exista en el DataFrame
    if "Match_id" not in df_reales.columns:
        df_reales["match_id"] = 0  # Crear la columna y llenarla inicialmente con 0

    # Define un umbral de similitud, por ejemplo, 80%
    threshold = 80

    # Convertir columnas en listas para optimizar el acceso
    nombres_goleadores = df_reales["NOMBRE"].tolist()
    nombres_fifa_sort = df_fifa["short_name"].tolist()
    nombres_fifa_long = df_fifa["long_name"].tolist()
    ids_fifa = df_fifa["sofifa_id"].tolist()

    # Recorrer los nombres de los goleadores
    for i, elemento in enumerate(nombres_goleadores):
        match_found = False  # Bandera para verificar si se encontró un match
        # Primera comprobación: comparación exacta
        for j, elemento2 in enumerate(nombres_fifa_long):
            if elemento == elemento2:  # Comparación exacta
                df_reales.at[i, "match_id"] = ids_fifa[j]  # Asignar el ID correspondiente
                match_found = True
                nombres_goleadores.pop(elemento)
                nombres_fifa_long.pop(elemento2)
                break  # Romper el bucle interno porque ya encontramos el match
            else:
                # Comparación fuzzy ignorando el orden de las palabras
                ratio = fuzz.token_sort_ratio(elemento, elemento2)
                if ratio >= threshold:  # Verificar si la similitud es mayor o igual al umbral
                    df_reales.at[i, "match_id"] = ids_fifa[j]  # Asignar el ID correspondiente
                    match_found = True
                    nombres_goleadores.pop(elemento)
                    nombres_fifa_long.pop(elemento2)
                    break  # Romper el bucle interno porque ya encontramos el match

        if not match_found:
            df_reales.at[i, "match_id"] = 0  # Si no se encontró un match, asignar 0
        
    for i, valor in df_reales["match_id"]:
        if i == 0:
            continue
        else:
        
"""
            