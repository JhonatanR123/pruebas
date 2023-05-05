import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import seaborn as sns
from scipy.interpolate import interp1d

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

valores=renombra("fem=f(t)/fem_agarre_abajo.csv")

def ajuste(datos,col):
    valores2=datos[col]
    valores3=[]
    for i in range(1,len(valores2)-1,3):
        valores3.append((valores2[i]+valores2[i-1]+valores2[i+1])/3)
        
    return(valores3)
        
valores_fem_ajustados=ajuste(valores,'columna_2')
valores_fem_ajustados.insert(0,valores.iloc[0]['columna_2'])
valores_fem_ajustados.append(valores.iloc[-1]['columna_2'])
valores_tiempo_ajustados=ajuste(valores,'columna_1')
valores_tiempo_ajustados.insert(0,valores.iloc[0]['columna_1'])
valores_tiempo_ajustados.append(valores.iloc[-1]['columna_1'])

v=0.581
mu_sub_cero=1.256e-6
N=31
mu=0.5829
L=0.0052
R=0.0125
t_0=1.231

fem1=(v*N*mu_sub_cero*mu*pow(R,2)/2*L)*((1/pow((pow((v*(t_0)+L/2),2)+pow(R,2)),3/2))-(1/pow(pow(v*t_0-L/2,2)+pow(R,2),3/2)))
# fem2=v*N*mu_sub_cero*mu*R^2/(2*L)*(1/(pow(pow(v*(t_0)+L/2),2)+pow(R,2)),(3/2))- (1/pow((pow(v*(t_0)-L/2),2)+pow(R,2),(3/2)))
valores_fem_teoricos=[]
tiempo=[]
j=0
for i in range(1075, 1800):
    i=i+1
    j=j+1
    t_rango=1.1781+(j*0.0009)
    tiempo.append(t_rango)
    valores_fem_teoricos.append(((v*N*mu_sub_cero*mu*pow(R,2))/(2*L))*(pow((pow(v*(t_rango-t_0)+L/2,2)+pow(R,2)),(3/2)) - pow((pow(v*(t_rango-t_0)-L/2,2)+pow(R,2)),(3/2))))

print(tiempo)

# print(valores_fem_teoricos)

print(len(valores_tiempo_ajustados))
print(len(valores_fem_ajustados))
sns.set(style='ticks', palette='pastel')
fig, ax = plt.subplots(figsize=(8,16))
sns.lineplot(x=valores['columna_1'],y=valores['columna_2'],linewidth=1)
# sns.lineplot(x=tiempo,y=valores_fem_teoricos,linewidth=1, color='red')
sns.lineplot(x=valores_tiempo_ajustados,y=valores_fem_ajustados,linewidth=1)
ax.set_xlabel('t(s)')
ax.set_ylabel('FEM(V)')
ax.set_title('FEM=f(t)')
plt.axhline(0, color='black', lw=0.5)
plt.axvline(0, color='black', lw=0.5)



plt.show()
