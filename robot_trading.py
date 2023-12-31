# -*- coding: utf-8 -*-
"""Robot_Trading.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v_GknGx5mZ3ds7sO4SrM6OBJeKAyfIw4

# 1. Configuración del Ambiente
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from bs4 import BeautifulSoup
import requests
from IPython.core.display import clear_output
import time

"""#2. Obtención de Datos

**Precios Históricos del Bitcoin**
"""

def importar_base_bitcoin():
  global df_bitcoin, precio_actual, tendencia, media_bitcoin, algoritmo_decision
  #Extraigo el historial por 7 dias con intervalo de 5 min del BTC-USD de la pagina yahoo finance mediante web scraping
  precios = yf.Ticker('BTC-USD')
  df_bitcoin= pd.DataFrame(precios.history(period='7d',interval='5m'))
  df_bitcoin = df_bitcoin[['Open','High','Low','Close','Volume']]

importar_base_bitcoin()
df_bitcoin.head()

"""**Indicadores de Tendencias**"""

def extraer_tendencias():
  global df_bitcoin, precio_actual, tendencia, media_bitcoin,  algoritmo_decision
  #Extraigo el valor actual y la tendencia del BTC de la pagina coinmarketcap mediante web scraping
  precios = yf.Ticker('BTC-USD')
  headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
  url = 'https://coinmarketcap.com/es/'
  respuesta = requests.get(url,headers = headers)

  s = BeautifulSoup(respuesta.content, features='lxml')
  precio_actual = s.findAll('div', {'class':['sc-a0353bbc-0 gDrtaY','sc-a0353bbc-0 gDrtaY fall', 'sc-a0353bbc-0 gDrtaY rise']}, limit=1)
  for i in precio_actual:
    precio_actual = i.text.strip().replace('$', '').replace(',', '')
    precio_actual = float(precio_actual)

  lista=[]
  tendencia =s.findAll('span', {'class':['sc-d55c02b-0 iwhBxy' , 'sc-d55c02b-0 gUnzUB']})
  for item in tendencia[::3] :
    lista.append(item)
  for indice in range(len(lista)):
    if lista[indice].find('span')['class'][0] == 'icon-Caret-down':
      tendencia = 'Baja'
    else:
        tendencia= 'Alta'

extraer_tendencias()
print('Precio Actual del Bitcoin:', precio_actual)
print('Tendencia del Mercado:', tendencia)

"""#3. Limpieza de Datos"""

def limpieza_datos() :
  global df_bitcoin, precio_actual, tendencia, media_bitcoin,  algoritmo_decision , df_bitcoin_sin_tratar ,df_bitcoin_limpio
  df_bitcoin_sin_tratar = df_bitcoin.copy()#creo una copia del original para poder trabajar en la limpieza
  df_bitcoin_sin_tratar = df_bitcoin_sin_tratar.reset_index()#creo un index para poder trabajar con la columna 'Datetime'

  #Trabajo la columna 'Datetime' si hay duplicados
  duplicados = df_bitcoin_sin_tratar['Datetime']
  if duplicados.duplicated().sum() > 0 :#pregunto si hay duplicados > a 0 , en ese caso procedo a la limpieza
    duplicados.drop_duplicates(inplace=True)
    df_bitcoin_sin_tratar = df_bitcoin_sin_tratar[duplicados]
    df_bitcoin_sin_tratar.index = range(len(df_bitcoin_sin_tratar))#le asigno un index ordenado

  #Trabajo la columna 'Close' si hay nulos
  if df_bitcoin_sin_tratar['Close'].isnull().sum() > 0 :#pregunto si hay nulos > a 0 , en ese caso procedo al tratamiento
    df_bitcoin_sin_tratar.fillna(method='ffill' , inplace='True')#relleno con el valor anterior los nulos

  #Trabajo columna 'Volumen'
  volumen_mayor_cero = (df_bitcoin_sin_tratar['Volume']> 0)#Creo una condición para eliminar las filas donde el volumen == 0
  df_bitcoin_sin_tratar = df_bitcoin_sin_tratar[volumen_mayor_cero]
  df_bitcoin_sin_tratar.index = range(len(df_bitcoin_sin_tratar))#le asigno un index ordenado

  #Elimino los outliers
  df_bitcoin_limpio = df_bitcoin_sin_tratar
  datos = (df_bitcoin_limpio['Close'].describe()).round(0)
  df = (df_bitcoin_limpio['Close']>datos[3]) & (df_bitcoin_limpio['Close']<datos[7])

  #Filtro los datos entre el primer y tercer cuartil
  df_bitcoin_limpio = df_bitcoin_limpio[df]
  df = (df_bitcoin_limpio['Close']>datos[4]) & (df_bitcoin_limpio['Close']<datos[6])
  df_bitcoin_limpio = df_bitcoin_limpio[df]

  #Calculo la media
  media_bitcoin = df_bitcoin_limpio['Close'].mean().round(0)

limpieza_datos()
df_bitcoin_sin_tratar.boxplot(['Close'])
plt.title('Grafico de Caja Sin Tratamiento')
plt.show()
df_bitcoin_limpio.boxplot(['Close'])
plt.title('Grafico de Caja con Tratamiento')
plt.show()

"""#4. Tomar Decisiones"""

def tomar_decisiones():
  global df_bitcoin, precio_actual, tendencia, media_bitcoin,  algoritmo_decision
  #Creo una condiciones
  if (precio_actual >= media_bitcoin) & (tendencia == 'Baja'):
    algoritmo_decision = 'Vender'
  elif (precio_actual < media_bitcoin) & (tendencia == 'Alta'):
    algoritmo_decision = 'Comprar'
  else:
    algoritmo_decision = 'Esperar'

"""#5. Visualización"""

def visualizacion():
  global df_bitcoin, precio_actual, tendencia, media_bitcoin,  algoritmo_decision

  #Adiciono una columna nueva con el valor de la media
  df_bitcoin['Promedio'] = media_bitcoin

  tomar_decisiones()
  print('Precio Promedio Bitcoin:', media_bitcoin)
  print('Precio Actual Bitcoin:', precio_actual)
  print('Tendencia:', tendencia)

  #Grafico
  plt.figure(figsize = (16,5))
  plt.title('Precio del Bitcoin ($)', fontsize = 25 , loc = 'left')
  df_bitcoin = df_bitcoin.reset_index()
  plt.plot(df_bitcoin['Datetime'],df_bitcoin['Close'])
  plt.axhline(y = media_bitcoin , color = 'r', linestyle = '-', xmin=0.05, xmax=0.95)
  plt.xlabel('Ultimos 7 dias de cotización')
  plt.ylabel('Precio del cierre de la cotizacón')
  legend_labels = ['Algoritmo de decisión: ' + algoritmo_decision, 'Promedio: ' + str(media_bitcoin)]
  plt.legend(legend_labels, loc='upper right')
  plt.show()

"""#6. Automatización"""
def principal():
    while(True):
      clear_output()
      importar_base_bitcoin()
      extraer_tendencias()
      limpieza_datos()
      tomar_decisiones()
      visualizacion()
      time.sleep(300)

principal()        
