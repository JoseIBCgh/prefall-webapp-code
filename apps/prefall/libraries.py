import pandas as pd
import numpy as np
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from collections import defaultdict
from scipy.interpolate import UnivariateSpline
import math
import itertools
import glob
import io
import warnings

import matplotlib.pyplot as plt

def filtro_acelerometro(datos):
    #
    # datos:    dataframe con los datos de tiempo (time) y acelerómetro (x, y, z)
    #
    
    # Copia de datos originales
    datos1 = datos.copy(deep = True)
    
    if np.mean(datos.ay) > 0:
        datos1.ay = -datos1.ay
    
    ind_x = np.where((datos1.ax >= np.mean(datos1.ax) + 8*np.std(datos1.ax)) | (datos1.ax <= np.mean(datos1.ax) - 8*np.std(datos1.ax)))
    ind_y = np.where((datos1.ay >= np.mean(datos1.ay) + 8*np.std(datos1.ay)) | (datos1.ay <= np.mean(datos1.ay) - 8*np.std(datos1.ay)))
    ind_z = np.where((datos1.az >= np.mean(datos1.az) + 8*np.std(datos1.az)) | (datos1.az <= np.mean(datos1.az) - 8*np.std(datos1.az)))
    
    if len(ind_x[0]) > 0:
        datos1.ax.iloc[ind_x] = np.nan
        datos1.ax = datos1.ax.interpolate(method ='linear', limit_direction ='both')
    if len(ind_y[0]) > 0:
        datos1.ay.iloc[ind_y] = np.nan
        datos1.ay = datos1.ay.interpolate(method ='linear', limit_direction ='both')
    if len(ind_z[0]) > 0:
        datos1.az.iloc[ind_z] = np.nan
        datos1.az = datos1.az.interpolate(method ='linear', limit_direction ='both')
    
    return datos1
    
def fases_marcha_individual(datos):
    #
    # datos:    dataframe con los datos de tiempo (time) y acelerómetro (x, y, z)
    #
    
    # datos_temp = datos1[['timestamp','ax','ay','az']].iloc[ind_temp].copy()
    # datos1 = datos_temp.copy(deep = True)
    
    # Copia de datos originales
    datos1 = datos.copy(deep = True)
        
    # Transformación a media cero las medidas
    datos1['ax'] = datos1['ax'] - np.mean(datos1['ax'])
    datos1['ay'] = datos1['ay'] - np.mean(datos1['ay'])
    datos1['az'] = datos1['az'] - np.mean(datos1['az'])
    
    #
    # Identificación de fases 1/3 vs 2/4
    #
    
    # Datos eje Y suavizados con 30 grados de libertad ¿?
    vector_temp = datos1['ay'].copy()
    ind_no_nas = np.where(-np.isnan(vector_temp))[0]
    vector_temp[np.isnan(vector_temp)] = 0
    ss = UnivariateSpline(ind_no_nas, vector_temp.iloc[ind_no_nas], k = 3, s = 1.75)
    datos1['ay_ss'] = np.nan
    datos1['ay_ss'].iloc[np.where(-np.isnan(datos1['ay']))] = ss(ind_no_nas)
    
    # Identificación de fases en función de la variable ay_ss
    signos_temp = np.sign(datos1['ay_ss'] + np.percentile(datos1['ay_ss'], 60))
    ind_signo = np.asarray(signos_temp.iloc[1:]) - np.asarray(signos_temp.iloc[:-1])
    ind_signo_pos = np.where(ind_signo != 0)[0] + 1
    fases = pd.DataFrame()
    fases['inicio'] = np.asarray(ind_signo_pos[:-1])
    fases['fin'] = np.asarray(ind_signo_pos[1:])
    fases['signo'] = np.sign(ind_signo[ind_signo != 0])[:-1]
    
    faaases=ss
    
    if fases.shape[0] == 0:
        return np.empty(datos.shape[0])
    
    #
    # Identificación de fases 1/2 vs 3/4
    #
    
    # Análisis a partie del eje X
    fases['lado'] = np.nan
    fases['valor'] = np.nan
    for i in range(0,fases.shape[0]):
        if fases['signo'].iloc[i] == 1:
            media_temp = round(np.mean([fases['inicio'].iloc[i], fases['fin'].iloc[i]]))
            ind_temp2 = list(set(range(0,datos.shape[0])) & set(range(-10 + media_temp,11 + media_temp)))
            fases['valor'].iloc[i] = np.mean(datos1['ax'].iloc[ind_temp2])
        
    if not all(np.isnan(fases['valor'])):
        ind_max = np.argmax(abs(fases['valor']))
        sign_temp = np.sign(fases['valor'].iloc[ind_max])
        fases['lado'] = np.append(np.resize([-sign_temp,-sign_temp,sign_temp,sign_temp], ind_max)[::-1],
                                  np.resize([sign_temp,sign_temp,-sign_temp,-sign_temp], fases.shape[0] - ind_max)[::-1])
    
    #
    # Asociación
    #
    
    # Identificación de estado en cada fase
    fases['estado'] = np.nan
    fases['estado'].loc[(fases['signo'] == 1)*(fases['lado'] == 1)] = 1
    fases['estado'].loc[(fases['signo'] == -1)*(fases['lado'] == 1)] = 2
    fases['estado'].loc[(fases['signo'] == 1)*(fases['lado'] == -1)] = 3
    fases['estado'].loc[(fases['signo'] == -1)*(fases['lado'] == -1)] = 4
    
    # Asociación de estados a los datos
    datos1['estado'] = np.nan
    for i in range(0,fases.shape[0]):
        datos1['estado'].iloc[range(fases['inicio'].iloc[i],fases['fin'].iloc[i] + 1)] = fases['estado'].iloc[i]
    
    return datos1['estado'],datos1['ay_ss'],faaases

def split(x, f):
    res = defaultdict(list)
    for v, k in zip(x, f):
        res[k].append(v)
    return res

def fases_marcha_global(datos):
    #
    # datos:    dataframe con los datos de tiempo (time) y acelerómetro (x, y, z)
    #
    
    # Copia de datos originales
    datos1 = datos.copy(deep = True)
    
    # Identificación de tramos
    ind_cambio = np.append(0, np.where(np.asarray(datos1['caminar'].iloc[1:]) -
                                       np.asarray(datos1['caminar'].iloc[:-1]) != 0)[0] + 1)
    
    # datos.to_csv('test.csv')
    
    if datos1['caminar'].iloc[0] == 0:
        ind_cambio = ind_cambio[1:]
    
    if (len(ind_cambio) % 2) == 1:
        ind_cambio = np.append(ind_cambio, ind_cambio[0])
    
    tramos = ind_cambio.copy().reshape(-1,2)
    tramos[:,1] = tramos[:,1] - 1 
    
    # Rastreo por tramo
    datos1['estado1'] = np.nan
    datos1['estado2'] = np.nan
    
    for i in range(0,tramos.shape[0]):
        # Filtro de outliers por tramo
        datos1.iloc[tramos[i,0]:(tramos[i,1] + 1)] = filtro_acelerometro(datos1.iloc[tramos[i,0]:(tramos[i,1] + 1)])
        
        # Partición y rastreo
        ind_part = max(1,round((tramos[i,1] - tramos[i,0])/700))
        vec_part = [j % ind_part for j in range(tramos[i,0],(tramos[i,1] + 1))]
        vec_part.sort()
        particiones = split(range(tramos[i,0],(tramos[i,1] + 1)), vec_part)
        
        for j in range(0,len(particiones)):
            if j == 0:
                ind_temp = range(particiones[j][0], particiones[j][-1] + 50)
            elif j == len(particiones):
                ind_temp = range(particiones[j][0] - 50, particiones[j][-1])
            else:
                ind_temp = range(particiones[j][0] - 50, particiones[j][-1] + 50)
            
            ind_temp = list(set(ind_temp) & set(range(0,datos1.shape[0])))
            est_temp,suav,faaases = fases_marcha_individual(datos1[['ax','ay','az']].iloc[ind_temp])
            if j % 2 == 1:
                datos1['estado1'].iloc[ind_temp] = est_temp
            else:
                datos1['estado2'].iloc[ind_temp] = est_temp
    
    # Unificación de estados
    datos1['estado'] = np.nan
    ind_eq = np.where(np.logical_or(datos1['estado1'] == datos1['estado2'], 
                      np.logical_and(np.isnan(datos1['estado1']), np.isnan(datos1['estado2']))))[0]
    datos1['estado'].iloc[ind_eq] = datos1['estado1'].iloc[ind_eq]
    
    ind_1 = np.where(np.logical_and(-np.isnan(datos1['estado1']), np.isnan(datos1['estado2'])))[0]
    datos1['estado'].iloc[ind_1] = datos1['estado1'].iloc[ind_1]
    
    ind_2 = np.where(np.logical_and(np.isnan(datos1['estado1']), -np.isnan(datos1['estado2'])))[0]
    datos1['estado'].iloc[ind_2] = datos1['estado2'].iloc[ind_2]
    
    ind_dif = np.where(np.logical_and(np.logical_and(-np.isnan(datos1['estado1']), 
                                                     -np.isnan(datos1['estado2'])), 
                                      datos1['estado1'] != datos1['estado2']))[0]
    datos1['estado'].iloc[ind_dif] = np.nan
    
    # Completitud de esados si el tramo sin datos es menor de 10 valores y tiene coherencia en la transición de estados
    if 1==1:
        ind_na = np.where(-np.isnan(datos1['estado']))[0]
        ind_na2 = np.where(np.logical_and(ind_na[1:] - ind_na[:-1] <= 10, ind_na[1:] - ind_na[:-1] > 1))[0]
        if len(ind_na2) > 0:
            for i in range(0,len(ind_na2)):
                ind_temp = range(ind_na[ind_na2[i]]+1,ind_na[ind_na2[i]+1])
                if (datos1['estado'].iloc[ind_na[ind_na2[i]+1]] - datos1['estado'].iloc[ind_na[ind_na2[i]]]) in [1,-3]:
                    if len(ind_temp) == 1: # i = 0
                        datos1['estado'].iloc[ind_temp] = datos1['estado'].iloc[ind_na[ind_na2[i]]].copy()
                    elif np.logical_and(len(ind_temp) % 2 == 1, len(ind_temp) != 1): # i = 10
                        datos1['estado'].iloc[ind_temp[:math.ceil(len(ind_temp)/2)]] = datos1['estado'].iloc[ind_na[ind_na2[i]]].copy()
                        datos1['estado'].iloc[ind_temp[math.ceil(len(ind_temp)/2):]] = datos1['estado'].iloc[ind_na[ind_na2[i] + 1]].copy()
                    elif len(ind_temp) % 2 == 0: # i = 3
                        datos1['estado'].iloc[ind_temp[:int(len(ind_temp)/2)]] = datos1['estado'].iloc[ind_na[ind_na2[i]]].copy()
                        datos1['estado'].iloc[ind_temp[int(len(ind_temp)/2):]] = datos1['estado'].iloc[ind_na[ind_na2[i] + 1]].copy()
    
    # Eliminación de tramos de marcha inferiores a 2 segundos
    if 1==2:
        ind_na = np.where(np.isnan(datos1['estado']))[0]
        ind_na2 = np.where(np.logical_and(ind_na[1:] - ind_na[:-1] <= 200, ind_na[1:] - ind_na[:-1] > 1))[0]
        if len(ind_na2) > 0:
            for i in range(0,len(ind_na2)):
                ind_temp = range(ind_na[ind_na2[i]]+1,ind_na[ind_na2[i]+1])
                datos1['estado'].iloc[ind_temp] = np.nan
    
    return datos1['estado']

#Función para generar el dataframe resumen de los datos de entrenamiento
def genera_df_train(resumen_casos,directorio="./datos/CTIC_casos/"):
    
    #Esqueleto del dataframe generado
    datos_final = pd.DataFrame(columns=[
                                    'duracion_f1',
                                    'ax_mean_f1', 'ay_mean_f1', 'az_mean_f1',
                                    'ax_std_f1', 'ay_std_f1', 'az_std_f1',
                                    'lax_mean_f1', 'lay_mean_f1', 'laz_mean_f1',
                                    'lax_std_f1', 'lay_std_f1', 'laz_std_f1',
                                    'gx_mean_f1', 'gy_mean_f1', 'gz_mean_f1',
                                    'gx_std_f1', 'gy_std_f1', 'gz_std_f1',
                                    'mx_mean_f1', 'my_mean_f1', 'mz_mean_f1',
                                    'mx_std_f1', 'my_std_f1', 'mz_std_f1',
                                    'duracion_f2',
                                    'ax_mean_f2', 'ay_mean_f2', 'az_mean_f2',
                                    'ax_std_f2', 'ay_std_f2', 'az_std_f2',
                                    'lax_mean_f2', 'lay_mean_f2', 'laz_mean_f2',
                                    'lax_std_f2', 'lay_std_f2', 'laz_std_f2',
                                    'gx_mean_f2', 'gy_mean_f2', 'gz_mean_f2',
                                    'gx_std_f2', 'gy_std_f2', 'gz_std_f2',
                                    'mx_mean_f2', 'my_mean_f2', 'mz_mean_f2',
                                    'mx_std_f2', 'my_std_f2', 'mz_std_f2',
                                    'duracion_f3',
                                    'ax_mean_f3', 'ay_mean_f3', 'az_mean_f3',
                                    'ax_std_f3', 'ay_std_f3', 'az_std_f3',
                                    'lax_mean_f3', 'lay_mean_f3', 'laz_mean_f3',
                                    'lax_std_f3', 'lay_std_f3', 'laz_std_f3',
                                    'gx_mean_f3', 'gy_mean_f3', 'gz_mean_f3',
                                    'gx_std_f3', 'gy_std_f3', 'gz_std_f3',
                                    'mx_mean_f3', 'my_mean_f3', 'mz_mean_f3',
                                    'mx_std_f3', 'my_std_f3', 'mz_std_f3',
                                    'duracion_f4',
                                    'ax_mean_f4', 'ay_mean_f4', 'az_mean_f4',
                                    'ax_std_f4', 'ay_std_f4', 'az_std_f4',
                                    'lax_mean_f4', 'lay_mean_f4', 'laz_mean_f4',
                                    'lax_std_f4', 'lay_std_f4', 'laz_std_f4',
                                    'gx_mean_f4', 'gy_mean_f4', 'gz_mean_f4',
                                    'gx_std_f4', 'gy_std_f4', 'gz_std_f4',
                                    'mx_mean_f4', 'my_mean_f4', 'mz_mean_f4',
                                    'mx_std_f4', 'my_std_f4', 'mz_std_f4',
                                    'riesgo'
                                    ])
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        #conjunto de train
        for i in range(len(resumen_casos)):
            caso=resumen_casos.iloc[i]
            dir_caso=directorio+str(caso["Caso"])+'/'
            #df_actual=libraries.df_from_txt(dir_caso)
            for fichero in glob.glob(dir_caso + '/*.txt'):
                # Abrir el archivo en modo lectura
                with open(fichero, 'r') as f:
                    # Leer el contenido del archivo
                    contenido = f.read()

                # Reemplazar los tabuladores por espacios en memoria
                contenido = contenido.replace('\t', ' ')

                # Crear un objeto DataFrame de Pandas a partir del contenido
                datos = pd.read_csv(io.StringIO(contenido), delim_whitespace=True)

                #Si el fichero está vacío lo pasamos
                if datos.empty:
                    continue

                #Renombramos columnas para adaptarlo al script libraries
                datos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)
                datos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)
                datos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)

                # Filtro de outliers general. Saltamos los primeros segundos para eliminar datos anomalos
                datos = filtro_acelerometro(datos.iloc[500:-500, :])

                #Definimos que el sujeto está caminando durante todo el proceso de medición. *A futuro esto puede modificarse
                datos['caminar'] = [1 for i in range(len(datos))]

                #Obtenemos las fases de la marcha
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    # Filtro de tramos caminados
                    if any(datos['caminar'] == 1):
                        if any(datos['caminar'][-10:] == 1):
                            datos['caminar'].iloc[-10:] = 0
                        datos['estado']=fases_marcha_global(datos)

                # Agrupa los datos por fases
                #datos=datos.dropna()
                fases = datos.groupby('estado')

                # Itera sobre cada grupo de fases
                fila = {}
                for i, (fase, grupo) in enumerate(fases, start=1):
                    # Calcula la duración de la fase
                    duracion = grupo['TIME'].iloc[-1] - grupo['TIME'].iloc[0]
                    duracion=len(grupo)/100

                    #acelerometro
                    ax_mean = grupo['ax'].mean()
                    ay_mean = grupo['ay'].mean()
                    az_mean = grupo['az'].mean()

                    ax_std = grupo['ax'].std()
                    ay_std = grupo['ay'].std()
                    az_std = grupo['az'].std()

                    #CALCULAMOS VALORES MEDIOS DE SENSORES PARA CADA FASE DE MARCHA
                    #Aceleracion lineal
                    lax_mean = grupo['LACC_X'].mean()
                    lay_mean = grupo['LACC_Y'].mean()
                    laz_mean = grupo['LACC_Z'].mean()

                    #giroscopio
                    gx_mean = grupo['GYR_X'].mean()
                    gy_mean = grupo['GYR_Y'].mean()
                    gz_mean = grupo['GYR_Z'].mean()

                    #magnetometro
                    mx_mean = grupo['MAG_X'].mean()
                    my_mean = grupo['MAG_Y'].mean()
                    mz_mean = grupo['MAG_Z'].mean()

                    #quaterniones
                    qx_mean = grupo['QUAT_X'].mean()
                    qy_mean = grupo['QUAT_Y'].mean()
                    qz_mean = grupo['QUAT_Z'].mean()
                    qw_mean = grupo['QUAT_Z'].mean()

                    #CALCULAMOS DESVIACION TIPICA DE SENSROES PARA CADA FASE DE MARCHA
                    #Aceleracion lineal
                    lax_std = grupo['LACC_X'].std()
                    lay_std = grupo['LACC_Y'].std()
                    laz_std = grupo['LACC_Z'].std()

                    #giroscopio
                    gx_std = grupo['GYR_X'].std()
                    gy_std = grupo['GYR_Y'].std()
                    gz_std = grupo['GYR_Z'].std()

                    #magnetometro
                    mx_std = grupo['MAG_X'].std()
                    my_std = grupo['MAG_Y'].std()
                    mz_std = grupo['MAG_Z'].std()

                    #quaterniones
                    qx_std = grupo['QUAT_X'].std()
                    qy_std = grupo['QUAT_Y'].std()
                    qz_std = grupo['QUAT_Z'].std()
                    qw_std = grupo['QUAT_Z'].std()
                    
                    #Riesgo
                    ri=0
                    if "Riesgo" in caso["Valoración"]:
                        ri=1

                    # Agrega las características al diccionario fila
                    fila.update({
                        'duracion_f'+str(i): duracion,
                        'ax_mean_f'+str(i): ax_mean, 'ay_mean_f'+str(i): ay_mean, 'az_mean_f'+str(i): az_mean,
                        'ax_std_f'+str(i): ax_std, 'ay_std_f'+str(i): ay_std, 'az_std_f'+str(i): az_std,
                        'lax_mean_f'+str(i): lax_mean, 'lay_mean_f'+str(i): lay_mean, 'laz_mean_f'+str(i): laz_mean,
                        'lax_std_f'+str(i): lax_std, 'lay_std_f'+str(i): lay_std, 'laz_std_f'+str(i): laz_std,
                        'gx_mean_f'+str(i): gx_mean, 'gy_mean_f'+str(i): gy_mean, 'gz_mean_f'+str(i): gz_mean,
                        'gx_std_f'+str(i): gx_std, 'gy_std_f'+str(i): gy_std, 'gz_std_f'+str(i): gz_std,
                        'mx_mean_f'+str(i): mx_mean, 'my_mean_f'+str(i): my_mean, 'mz_mean_f'+str(i): mz_mean,
                        'mx_std_f'+str(i): mx_std, 'my_std_f'+str(i): my_std, 'mz_std_f'+str(i): mz_std,
                        'riesgo':ri
                    })

                # Convierte la fila en un DataFrame y añade la fila al dataframe final
                df_fila = pd.DataFrame([fila])
                datos_final = pd.concat([datos_final, df_fila], ignore_index=True)

    #Convertimos la variable objetivo a entero para que el modelo pueda entenderlo
    datos_final['riesgo']=datos_final['riesgo'].astype(int)
    return datos_final

def genera_grafica_fases(dir_fichero,intervalo):
    try:
        # Abrir el archivo en modo lectura
        with open(dir_fichero, 'r') as f:
            # Leer el contenido del archivo
            contenido = f.read()
    except Exception as e:
        print("Ha habido un error con el fichero:")
        print(e)
        exit(1)

    # Reemplazar los tabuladores por espacios en memoria
    contenido = contenido.replace('\t', ' ')

    # Crear un objeto DataFrame de Pandas a partir del contenido
    elementos = pd.read_csv(io.StringIO(contenido), delim_whitespace=True)
    elementos = elementos.reset_index()

    #Renombramos columnas para adaptarlo al script libraries
    elementos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)
    elementos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)
    elementos.rename(columns={'ACC_X': 'ax', 'ACC_Y': 'ay', 'ACC_Z': 'az'}, inplace=True)

    # Filtro de outliers general. Saltamos los primeros segundos para eliminar datos anomalos
    elementos = filtro_acelerometro(elementos.iloc[500:-500, :])

    #Definimos que el sujeto está caminando durante todo el proceso de medición. *A futuro esto puede modificarse
    elementos['caminar'] = [1 for i in range(len(elementos))]

    #Obtenemos las fases de la marcha
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # Filtro de tramos caminados
        if any(elementos['caminar'] == 1):
            if any(elementos['caminar'][-10:] == 1):
                elementos['caminar'].iloc[-10:] = 0
            elementos['estado']=fases_marcha_global(elementos)
    
    #Seleccionamos los elementos del intervalo de interés
    elementos=elementos.iloc[intervalo[0]:intervalo[1]]
    
    # Establecer colores para cada estado
    color_map = {
        1.0: "red",
        2.0: "red",
        3.0: "blue",
        4.0: "blue"
    }

    bri_map = {
        1.0: 0.45,
        2.0: 0.15,
        3.0: 0.15,
        4.0: 0.45
    }

    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar ax, ay y az
    ax.plot(elementos['ax'], label='ax', color="black")
    ax.plot(elementos['ay'], label='ay', color="black",linestyle='dashdot')
    ax.plot(elementos['az'], label='az', color="black",linestyle='dashed')

    # Agregar bandas de colores en función del estado
    for i, row in elementos.iterrows():
        ax.axvspan(i, i+1, facecolor=color_map[row['estado']], alpha=bri_map[row['estado']])

    ax.legend()
    plt.show()

#Función para definir todos los pasos de la medición
def assign_steps(s):
    step_counter = 1
    steps = []
    for idx, val in enumerate(s):
        # Si el estado actual no es 4.0 pero el anterior sí lo era, incrementamos el contador de pasos.
        if idx > 0 and val != 4.0 and s[idx-1] == 4.0:
            step_counter += 1
        steps.append(step_counter)
    return steps

# Port de la funcion genera_grafica_fases para un dataframe
def genera_grafica_fases_port(elementos, intervalo):
    elementos = elementos.reset_index()

    #Renombramos columnas para adaptarlo al script libraries
    elementos.rename(columns={'acc_x': 'ax', 'acc_y': 'ay', 'acc_z': 'az'}, inplace=True)

    elementos.rename(columns={'gyr_x': 'GYR_X', 'gyr_y': 'GYR_Y', 'gyr_z': 'GYR_Z'}, inplace=True)

    elementos.rename(columns={'mag_x': 'MAG_X', 'mag_y': 'MAG_Y', 'mag_z': 'MAG_Z'}, inplace=True)

    elementos.rename(columns={'lacc_x': 'LACC_X', 'lacc_y': 'LACC_Y', 'lacc_z': 'LACC_Z'}, inplace=True)

    elementos.rename(columns={'quat_x': 'QUAT_X', 'quat_y': 'QUAT_Y', 'quat_z': 'QUAT_Z', 'quat_w' : 'QUAT_W'}, inplace=True)
    
    elementos.rename(columns={'time': 'TIME'}, inplace=True)
    # Filtro de outliers general. Saltamos los primeros segundos para eliminar datos anomalos
    elementos = filtro_acelerometro(elementos.iloc[500:-500, :])

    #Definimos que el sujeto está caminando durante todo el proceso de medición. *A futuro esto puede modificarse
    elementos['caminar'] = [1 for i in range(len(elementos))]

    #Obtenemos las fases de la marcha
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # Filtro de tramos caminados
        if any(elementos['caminar'] == 1):
            if any(elementos['caminar'][-10:] == 1):
                elementos['caminar'].iloc[-10:] = 0
            elementos['estado']=fases_marcha_global(elementos)
    
    #Seleccionamos los elementos del intervalo de interés
    if intervalo:
        elementos=elementos.iloc[intervalo[0]:intervalo[1]]
    
    import plotly.graph_objects as go

    # Define color and brightness maps
    color_map = {
        1.0: "red",
        2.0: "red",
        3.0: "blue",
        4.0: "blue"
    }

    bri_map = {
        1.0: 0.45,
        2.0: 0.15,
        3.0: 0.15,
        4.0: 0.45
    }
    """
    #BEGIN parte original, quitar
    #Es para comprobar que tira error igual
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar ax, ay y az
    ax.plot(elementos['ax'], label='ax', color="black")
    ax.plot(elementos['ay'], label='ay', color="black",linestyle='dashdot')
    ax.plot(elementos['az'], label='az', color="black",linestyle='dashed')

    # Agregar bandas de colores en función del estado
    for i, row in elementos.iterrows():
        ax.axvspan(i, i+1, facecolor=color_map[row['estado']], alpha=bri_map[row['estado']])

    # END parte original quitar
    """
    # Create a Plotly figure
    fig = go.Figure()

    # Plot ax, ay, and az
    fig.add_trace(go.Scatter(x=elementos.index.to_list(), y=elementos['ax'].to_list(), mode='lines', name='ax', line=dict(color="black")))
    fig.add_trace(go.Scatter(x=elementos.index.to_list(), y=elementos['ay'].to_list(), mode='lines', name='ay', line=dict(color="black", dash='dashdot')))
    fig.add_trace(go.Scatter(x=elementos.index.to_list(), y=elementos['az'].to_list(), mode='lines', name='az', line=dict(color="black", dash='dash')))

    # Add color bands based on the state
    for i, row in elementos.iterrows():
        if not np.isnan(row['estado']):
            fig.add_shape(
                type='line',
                x0=i,
                x1=i,
                y0=0, 
                y1=1,
                line=dict(color=color_map[row['estado']], width=1),
                opacity=bri_map[row['estado']],
                xref='x',
                yref='paper',
                layer="below",
            )
    # Add legend
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig

def genera_metricas_port(elementos):
    elementos = elementos.reset_index()

    #Renombramos columnas para adaptarlo al script libraries
    elementos.rename(columns={'acc_x': 'ax', 'acc_y': 'ay', 'acc_z': 'az'}, inplace=True)

    elementos.rename(columns={'gyr_x': 'GYR_X', 'gyr_y': 'GYR_Y', 'gyr_z': 'GYR_Z'}, inplace=True)

    elementos.rename(columns={'mag_x': 'MAG_X', 'mag_y': 'MAG_Y', 'mag_z': 'MAG_Z'}, inplace=True)

    elementos.rename(columns={'lacc_x': 'LACC_X', 'lacc_y': 'LACC_Y', 'lacc_z': 'LACC_Z'}, inplace=True)

    elementos.rename(columns={'quat_x': 'QUAT_X', 'quat_y': 'QUAT_Y', 'quat_z': 'QUAT_Z', 'quat_w' : 'QUAT_W'}, inplace=True)
    
    elementos.rename(columns={'time': 'TIME'}, inplace=True)
    # Filtro de outliers general. Saltamos los primeros segundos para eliminar datos anomalos
    elementos = filtro_acelerometro(elementos.iloc[500:-500, :])

    #Definimos que el sujeto está caminando durante todo el proceso de medición. *A futuro esto puede modificarse
    elementos['caminar'] = [1 for i in range(len(elementos))]

    #Obtenemos las fases de la marcha
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        # Filtro de tramos caminados
        if any(elementos['caminar'] == 1):
            if any(elementos['caminar'][-10:] == 1):
                elementos['caminar'].iloc[-10:] = 0
            elementos['estado']=fases_marcha_global(elementos)
        elementos['Paso'] = assign_steps(elementos['estado'].to_numpy())
        
        #Agrupamos por fase
        fases = elementos.groupby('estado')

        # Itera sobre cada grupo de fases
        fila = {}
        fila.update({
                'duracion_total_medicion': elementos['TIME'].iloc[-1]+500 * 0.01, 'duracion_real_analizada': elementos['TIME'].iloc[-1]-500 * 0.01,
                'n_pasos_totales': elementos['Paso'].iloc[-1], 'n_pasos_minuto': elementos['Paso'].iloc[-1]/(elementos['TIME'].iloc[-1] / 60),
            })
        for i, (fase, grupo) in enumerate(fases, start=1):
            # Calcula la duración de la fase
            duracion = len(grupo['TIME'])
            duracion_porcentaje=duracion/len(elementos.dropna(subset=['estado']))
            duracion /= 100 #porque hay 100 paquetes por segundo
            #acelerometro
            ax_mean = grupo['ax'].mean()
            ay_mean = grupo['ay'].mean()
            az_mean = grupo['az'].mean()

            ax_std = grupo['ax'].std()
            ay_std = grupo['ay'].std()
            az_std = grupo['az'].std()

            #CALCULAMOS VALORES MEDIOS DE SENSORES PARA CADA FASE DE MARCHA
            #Aceleracion lineal
            lax_mean = grupo['LACC_X'].mean()
            lay_mean = grupo['LACC_Y'].mean()
            laz_mean = grupo['LACC_Z'].mean()

            #giroscopio
            gx_mean = grupo['GYR_X'].mean()
            gy_mean = grupo['GYR_Y'].mean()
            gz_mean = grupo['GYR_Z'].mean()

            #magnetometro
            mx_mean = grupo['MAG_X'].mean()
            my_mean = grupo['MAG_Y'].mean()
            mz_mean = grupo['MAG_Z'].mean()

            #quaterniones
            qx_mean = grupo['QUAT_X'].mean()
            qy_mean = grupo['QUAT_Y'].mean()
            qz_mean = grupo['QUAT_Z'].mean()
            qw_mean = grupo['QUAT_Z'].mean()

            #CALCULAMOS DESVIACION TIPICA DE SENSROES PARA CADA FASE DE MARCHA
            #Aceleracion lineal
            lax_std = grupo['LACC_X'].std()
            lay_std = grupo['LACC_Y'].std()
            laz_std = grupo['LACC_Z'].std()

            #giroscopio
            gx_std = grupo['GYR_X'].std()
            gy_std = grupo['GYR_Y'].std()
            gz_std = grupo['GYR_Z'].std()

            #magnetometro
            mx_std = grupo['MAG_X'].std()
            my_std = grupo['MAG_Y'].std()
            mz_std = grupo['MAG_Z'].std()

            #quaterniones
            qx_std = grupo['QUAT_X'].std()
            qy_std = grupo['QUAT_Y'].std()
            qz_std = grupo['QUAT_Z'].std()
            qw_std = grupo['QUAT_Z'].std()


            # Agrega las características al diccionario fila
            fila.update({
                'duracion_porcentaje_f'+str(i): duracion_porcentaje, 'duracion_total_f'+str(i): duracion,
                'ax_mean_f'+str(i): ax_mean, 'ay_mean_f'+str(i): ay_mean, 'az_mean_f'+str(i): az_mean,
                'ax_std_f'+str(i): ax_std, 'ay_std_f'+str(i): ay_std, 'az_std_f'+str(i): az_std,
                'lax_mean_f'+str(i): lax_mean, 'lay_mean_f'+str(i): lay_mean, 'laz_mean_f'+str(i): laz_mean,
                'lax_std_f'+str(i): lax_std, 'lay_std_f'+str(i): lay_std, 'laz_std_f'+str(i): laz_std,
                'gx_mean_f'+str(i): gx_mean, 'gy_mean_f'+str(i): gy_mean, 'gz_mean_f'+str(i): gz_mean,
                'gx_std_f'+str(i): gx_std, 'gy_std_f'+str(i): gy_std, 'gz_std_f'+str(i): gz_std,
                'mx_mean_f'+str(i): mx_mean, 'my_mean_f'+str(i): my_mean, 'mz_mean_f'+str(i): mz_mean,
                'mx_std_f'+str(i): mx_std, 'my_std_f'+str(i): my_std, 'mz_std_f'+str(i): mz_std,
            })

        # Convierte la fila en un DataFrame y añade la fila al dataframe final
        df_fila = pd.DataFrame([fila])

        return df_fila