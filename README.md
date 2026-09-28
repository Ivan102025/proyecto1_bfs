
# Explorador visual con búsqueda en amplitud (BFS)

Proyecto 1 - Fundamentos de Inteligencia Artificial
Universidad Tecnológica de la Huasteca Hidalguense

## Integrantes
- Iván (apellido) - Matrícula 20241110
- Isaí Pascual Cruz - Matrícula 20241018

## Versión de Python
Se desarrolló con Python 3.12, pero corre bien desde 3.9 en adelante.
El programa de escritorio (main.py) no usa ninguna librería externa,
solo lo que trae Python por defecto: tkinter, collections, random,
json, time, csv y pathlib.

El notebook de Colab (dentro de 02_codigo/modulos_y_notebooks/) además
usa matplotlib para dibujar las animaciones, ya que Colab no tiene
ventanas de escritorio. Esa librería ya viene instalada en Colab.

## Instalación
Para correr main.py no hay que instalar nada, solo se necesita Python
con tkinter. En Windows y en Mac ya viene incluido. En Linux, si no lo
tienes, se instala con:

    sudo apt install python3-tk

Para el notebook de Colab tampoco hay que instalar nada, con subirlo a
Google Colab es suficiente (matplotlib ya está ahí).

## Cómo ejecutar

Versión de escritorio:

    cd 02_codigo/modulos_y_notebooks
    python generar_mapas.py      (genera los 3 mapas de prueba)
    cd ..
    python main.py               (abre la interfaz gráfica)

Desde la interfaz se puede elegir el mapa en el menú de arriba y usar
los botones Iniciar / Pausar / Avanzar / Reiniciar, además del control
de velocidad.

Para las pruebas por consola (genera metricas.csv):

    cd 02_codigo/modulos_y_notebooks
    python ejecutar_pruebas.py

Versión Colab (la que se usó para grabar el video):
subir 02_codigo/modulos_y_notebooks/Proyecto1_BFS_Colab.ipynb a Google
Colab y correr las celdas en orden, de arriba hacia abajo. Las
instrucciones más detalladas están en Instrucciones_de_ejecucion.ipynb,
en la misma carpeta.

## Semillas
La semilla del mapa principal (y del mapa de estrés) sale de ordenar
alfabéticamente las matrículas de los dos integrantes y pegarlas:

    semilla = int("".join(sorted(["20241110", "20241018"])))
    # = 2024101820241110

Así, sin importar quién la escriba primero, siempre da la misma
semilla y por lo tanto el mismo mapa. Se puede correr generar_mapas.py
las veces que sea y el mapa principal siempre sale igual.

Para probar con otras matrículas hay que cambiar MATRICULA_1 y
MATRICULA_2 al inicio de main.py y de generar_mapas.py (y en la celda
correspondiente del notebook), y borrar los .json de
03_mapas/mapa_principal_y_pruebas/ para que se vuelvan a generar.

## Estructura
    02_codigo/
      main.py                    interfaz gráfica (escritorio)
      modulos_y_notebooks/
        bfs.py                   BFS: cola FIFO, parent, metricas
        maze.py                  generación y validación de mapas
        generar_mapas.py         genera y guarda los 3 mapas
        ejecutar_pruebas.py      corre BFS y genera metricas.csv
        Proyecto1_BFS_Colab.ipynb        notebook usado en el video
        Instrucciones_de_ejecucion.ipynb instrucciones para el notebook
    03_mapas/mapa_principal_y_pruebas/   mapas guardados en json
    04_resultados/
      metricas.csv
      capturas/
    05_evidencias/
      enlace_video.txt

## Resultados
| Mapa | Tamaño | Ruta óptima |
|---|---|---|
| Principal | 25x25, 28% obstáculos | 52 movimientos |
| Sencillo | 7x7 | 12 movimientos (comprobado a mano con la distancia Manhattan) |
| Estrés | 30x30, 35% obstáculos | 60 movimientos |

## Problemas conocidos
- main.py necesita un entorno con ventanas (no corre en un servidor sin
  pantalla ni en Colab). Para eso está el notebook.
- Los archivos que se guardan al correr el notebook en Colab (mapas y
  metricas.csv) se pierden si se reinicia el entorno de ejecución,
  porque Colab no los guarda de forma permanente. Hay que descargarlos
  si se quieren conservar.
- En mapas grandes la lista de la frontera se corta a los primeros 12
  elementos y se muestra el tamaño total, tal como pide la consigna.

## Declaración de uso de IA
Se usó Claude (Anthropic) como apoyo durante el desarrollo: para
revisar que el código cumpliera con lo que pide la consigna, para
simplificar partes que estaban muy extensas sin cambiar cómo se ve ni
cómo funciona, y para adaptar la visualización al notebook de Colab. El
algoritmo de BFS y la lógica de generación de mapas las escribimos
nosotros; se validó corriendo el programa completo, comparando el
resultado del mapa sencillo contra la distancia Manhattan calculada a
mano, y revisando que los mapas se sigan generando igual después de
descomprimir el proyecto en una carpeta nueva.