# Explorador visual con búsqueda en amplitud (BFS)

Proyecto 1 — Fundamentos de Inteligencia Artificial
Universidad Tecnológica de la Huasteca Hidalguense

## Integrantes
- Integrante 1 — Matrícula: 20241110
- Integrante 2 — Matrícula: 20241018

*(Completar con los nombres completos antes de entregar.)*

## Versión de Python
Desarrollado y probado con **Python 3.12**. Cualquier Python 3.9 o
superior debería funcionar, ya que el proyecto solo usa la biblioteca
estándar.

## Instalación
No se requieren paquetes externos: todo el proyecto usa únicamente la
biblioteca estándar de Python (`tkinter`, `collections`, `random`,
`json`, `time`, `csv`, `pathlib`).

```bash
# (opcional) crear un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

pip install -r requirements.txt   # no hay paquetes que instalar
```

> Nota: `tkinter` viene incluido con la instalación estándar de Python en
> Windows y macOS. En Linux, si no está disponible, se instala con
> `sudo apt install python3-tk` (Debian/Ubuntu).

## Estructura del proyecto
```
02_codigo/
  main.py              -> interfaz gráfica (Tkinter): visualización paso a paso
  bfs.py               -> implementación propia de BFS (cola FIFO, parent, métricas)
  maze.py              -> generación y validación de mapas (semilla, restricciones)
  generar_mapas.py     -> genera y guarda los 3 mapas de prueba en 03_mapas/
  ejecutar_pruebas.py  -> corre BFS sobre los 3 mapas y genera 04_resultados/metricas.csv
03_mapas/               -> mapas de prueba guardados en JSON (reproducibles)
04_resultados/          -> metricas.csv y capturas de pantalla
```

## Comando de ejecución

1. Generar (o regenerar) los tres mapas de prueba obligatorios:
   ```bash
   cd 02_codigo
   python generar_mapas.py
   ```

2. Abrir la interfaz gráfica:
   ```bash
   python main.py
   ```
   - **Menú desplegable**: elige el mapa (Mapa principal / Mapa sencillo /
     Mapa de estrés / Cargar archivo...).
   - **▶ Iniciar**: reproduce la búsqueda automáticamente.
   - **⏸ Pausar**: detiene la reproducción automática (puede reanudarse con Iniciar).
   - **⏭ Avanzar**: ejecuta un solo paso de BFS a la vez.
   - **⟲ Reiniciar**: vuelve al paso 0 con el mapa actualmente cargado.
   - El control deslizante ajusta la velocidad de la reproducción
     automática (más a la derecha = más rápido).
   - El panel derecho muestra en todo momento la leyenda de colores, la
     frontera en orden FIFO (truncada a los primeros 12 elementos con el
     tamaño total cuando es muy grande) y, al llegar a la meta o agotar
     la frontera, las métricas finales.

3. (Opcional) Ejecutar las pruebas por consola y generar el CSV de
   métricas usado como evidencia en el reporte:
   ```bash
   python ejecutar_pruebas.py
   ```
   Esto imprime resultados en pantalla y guarda
   `04_resultados/metricas.csv`.

## Semillas
La semilla del mapa principal (y del mapa de estrés) se construye
ordenando alfabéticamente las matrículas de ambos integrantes y
concatenándolas:

```python
semilla = int("".join(sorted(["20241110", "20241018"])))
        # = int("2024101820241110")
```

Esto garantiza que, sin importar el orden en que se escriban las
matrículas, ambos integrantes obtengan siempre la misma semilla y por lo
tanto el mismo mapa. Ejecutar `generar_mapas.py` cuantas veces se quiera
produce exactamente el mismo mapa principal (se comprobó de forma
automatizada: mismo `grid`, mismo resultado, en cualquier orden de las
matrículas).

Para usar otras matrículas, editar las constantes `MATRICULA_1` y
`MATRICULA_2` al inicio de `main.py` y `generar_mapas.py`, y borrar los
archivos `.json` de `03_mapas/` para que se regeneren.

## Resultados obtenidos (referencia)
| Mapa | Tamaño | % obstáculos | Ruta óptima | Verificación |
|---|---|---|---|---|
| Principal | 25×25 | 28.0% | 52 movimientos | BFS propio (cumple mínimo de 25) |
| Sencillo | 7×7 | — (muro con un hueco) | 12 movimientos | Coincide con distancia Manhattan calculada a mano |
| Estrés | 30×30 | 35.0% (límite superior exacto) | 60 movimientos | BFS propio |

## Decisiones de diseño
- BFS sigue el patrón de las Sesiones 7 y 8: `collections.deque` como
  frontera FIFO, un diccionario `parent` que funciona simultáneamente
  como registro de alcanzados **y** de padres (un estado se marca en el
  momento en que se agrega a la cola, no cuando se expande), y prueba de
  meta al **retirar** el nodo de la cola —tal como se explicó en clase
  para conservar la garantía de profundidad mínima real.
- No se utiliza `networkx`, `pathfinding`, `scipy` ni ninguna función que
  resuelva el camino directamente; toda la lógica de la cola, el
  filtrado de repetidos y la reconstrucción del camino está escrita en
  `bfs.py`.
- La generación del mapa reutiliza el propio BFS (no una librería) para
  medir la longitud de la ruta óptima y validar la restricción de 25
  movimientos mínimos.
- La visualización guarda, para cada paso de BFS, el nodo expandido, el
  contenido completo de la frontera y el conjunto de visitados; esto
  permite reproducir la búsqueda paso a paso sin volver a ejecutarla.

## Problemas conocidos
- La interfaz gráfica requiere un entorno con soporte de ventanas
  (Tkinter). En un servidor sin entorno gráfico no podrá abrirse
  `main.py`, pero sí pueden ejecutarse `generar_mapas.py` y
  `ejecutar_pruebas.py`, que no requieren interfaz.
- En mapas muy grandes, la lista de la frontera se trunca visualmente a
  los primeros 12 elementos (se indica el tamaño total), tal como pide
  la consigna.

## Declaración de uso de IA
*(Completar antes de entregar: herramienta utilizada, qué partes se
generaron con su ayuda, qué se modificó y cómo se validó el
funcionamiento — por ejemplo, la comparación del mapa sencillo contra la
distancia Manhattan calculada a mano.)*
