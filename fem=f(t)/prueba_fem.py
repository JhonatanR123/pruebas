import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Función para renombrar las columnas del archivo
def renombra(archivo):
    with open(archivo, 'r') as valores:
        contenido = valores.read()
        if '\t' in contenido:
            dataframe = pd.read_csv(archivo, sep='\t', decimal=',')
        elif ';' in contenido:
            dataframe = pd.read_csv(archivo, sep=';', decimal=',')
        else:
            raise ValueError('No se encontró un separador válido en el archivo')
        
        nombre_actual = dataframe.columns[0]
        dataframe = dataframe.rename(columns={nombre_actual: 'columna_1'})
        nombre_actual1 = dataframe.columns[1]
        dataframe = dataframe.rename(columns={nombre_actual1: 'columna_2'})
        
        return dataframe

# Leer el archivo y extraer las columnas de tiempo y voltaje
valores = renombra("fem=f(t)/fem_agarre_abajo.csv")
t = valores.iloc[:, 0]
v = valores.iloc[:, 1]

# Graficar la señal original
plt.plot(t, v, '-')

# Definir el rango de interés
rango_inicial = 0.8
rango_final = 1.2

# Obtener los índices correspondientes al rango de interés
idx_inicio = (t - rango_inicial).abs().idxmin()
idx_fin = (t - rango_final).abs().idxmin()

# Seleccionar el rango de interés y graficarlo
trango = t.iloc[idx_inicio:idx_fin]
vrango = v.iloc[idx_inicio:idx_fin]
plt.plot(trango, vrango, '-')

# Definir las constantes
v = 0.581
N = 31
uo = 4 * np.pi * 10 ** (-7)
m = 0.550
R = 0.026
L = 0.0026
to = 0

# Calcular la FEM teórica
fem_teorica = v * N * uo * m * R ** 2 / (2 * L) * (1 / ((v * (trango - to) + L / 2) ** 2 + R ** 2) ** (3 / 2) - 1 / ((v * (trango - to) - L / 2) ** 2 + R ** 2) ** (3 / 2))

# Calcular la FEM experimental
fem_experimental = np.gradient(vrango, trango) 

# Graficar la FEM teórica y experimental
plt.figure()
plt.plot(trango, fem_teorica, label='FEM teórica')
plt.plot(trango, fem_experimental, label='FEM experimental')
plt.legend()

plt.show()
