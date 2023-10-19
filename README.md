# **Robot Trading**
Este proyecto utiliza tecnologías como Python , Numpy , Matplotlib, Web Scraping y estrategias personalizadas para automatizar el análisis de datos en tiempo real
# **Breve Descripción del Proyecto**
**1. Configuración del Ambiente:**
Importa las bibliotecas necesarias, como pandas, numpy, matplotlib, yfinance, BeautifulSoup, requests, entre otras.

**2. Obtención de Datos:**
La función 'importar_base_bitcoin' obtiene los precios históricos del Bitcoin de los últimos 7 días con intervalo de 5 minutos desde Yahoo Finance y almacena los datos en un DataFrame llamado df_bitcoin.
La función extraer_tendencias extrae el precio actual y la tendencia del mercado del Bitcoin desde CoinMarketCap mediante web scraping y almacena estos valores en las variables globales precio_actual y tendencia.

**3. Limpieza de Datos:**
La función 'limpieza_datos' realiza varias operaciones de limpieza en el DataFrame df_bitcoin, como eliminar duplicados, rellenar valores nulos, filtrar datos con volumen mayor que cero y eliminar outliers. Los datos limpios se almacenan en df_bitcoin_limpio, y se calcula la media del precio del cierre, que se almacena en media_bitcoin.
Se muestran gráficos de caja antes y después de la limpieza de datos.

**4. Tomar Decisiones:**
La función 'tomar_decisiones' determina la acción a tomar (comprar, vender o esperar) en función de las condiciones definidas en el script, que incluyen el precio actual y la tendencia del mercado.

**5. Visualización:**
La función 'visualización' crea un gráfico que muestra el precio del Bitcoin en los últimos 7 días, la línea de precio promedio, la acción a tomar (comprar, vender o esperar) y otros detalles relevantes.

**6. Automatización:**
La función 'principal' ejecuta un bucle infinito que actualiza los datos, realiza análisis y toma decisiones cada 5 minutos utilizando las funciones anteriores. Se utiliza clear_output para borrar la salida anterior en Jupyter Notebook. El script se ejecuta continuamente, lo que permite tomar decisiones automatizadas en función de las condiciones del mercado.




