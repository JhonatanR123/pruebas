import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def promedio(archivo,col):
    col=col-1
    with open(archivo, 'r') as valores:
        contenido = valores.read()
        if '\t' in contenido:
            dataframe = pd.read_csv(archivo, sep='\t', decimal=',')
        elif ';' in contenido:
            dataframe = pd.read_csv(archivo, sep=';', decimal=',')
        else:
            raise ValueError('No se encontró un separador válido en el archivo')
        
        nombre_actual = dataframe.columns[col]
        dataframe = dataframe.rename(columns={nombre_actual: 'columna_2'})
        
        return(dataframe['columna_2'].mean())

def func(x, a,b):
    return [a/pow(xi,3)+b for xi in x]

archivos=["B=f(z)/B_a_10.csv","B=f(z)/B_a_15.csv","B=f(z)/B_a_20.csv","B=f(z)/B_a_25.csv","B=f(z)/B_a_30.csv","B=f(z)/B_a_35.csv"]
columna=2
promedios=[]
distancias=[0.10,0.15,0.20,0.25,0.30,0.35]
for archivo in archivos:
    promedios.append(promedio(archivo,columna))
for i in range (len(promedios)):
    promedios[i]/=1000
popt, pcov = curve_fit(func, distancias, promedios)
print('El valor del parámetro de ajuste es: {}'.format(popt)) 
# print(promedios)
plt.scatter(distancias,promedios)
x_fit = np.linspace(min(distancias), max(distancias), 1000)
plt.plot(x_fit, func(x_fit, *popt),'r-',label='Ajuste')

plt.title('B=f(x)')
plt.xlabel('x(m)')
plt.ylabel('B(T)')

plt.show()