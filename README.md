# Descripción
Este proyecto es una implementación del juego de mesa "Parques Tradicional" utilizando Python y la biblioteca Pygame para la interfaz gráfica. El juego sigue las reglas clásicas del parqués con cuatro jugadores (Rojo, Azul, Verde y Amarillo), donde cada jugador debe mover sus cuatro fichas desde la cárcel hasta la meta, pasando por un tablero exterior y una vía interna.
# Características
- Tablero clásico con 68 casillas externas y 8 casillas internas por jugador
- Sistema de turnos con lanzamiento de dados y movimiento de fichas**
- Mecánicas de juego completas:
    * Sacar fichas de la cárcel con 5
    * Captura de fichas enemigas (20 casillas bonus)
    * Movimientos bonus por capturas y entradas a la vía interna
    * Bloqueos con dos fichas del mismo color
    * Penalización por tres dobles consecutivos
    * Requisito de exactitud para entrar a la vía interna y meta
- Interfaz gráfica intuitiva con representación visual del tablero
     * Representación visual del tablero
     * Sistema de selección de fichas con clics
     * Dados interactivos
     * Panel de información
# Requisitos
- Python 3.6 o superior
- Biblioteca pygame ```pip install pygame```
# Instrucciones de Ejecución
1. Clona el repositorio o descarga el archivo ```parques.py```
2. Ejecuta el siguiente comando en tu terminal:
````python
python parques.py
````
# Controles del Juego
1. Clic izquierdo: Seleccionar fichas o dados
2. Botón "Lanzar dados": Lanzar los dados al inicio del turno
3. Botón "Terminar turno": Pasar al siguiente jugador
# Estructura del Código:
El código está organizado en las siguientes secciones principales:
   1. Parámetros Globales y Constantes
````python
NUM_CASILLAS_EXTERNAS = 68
NUM_CASILLAS_INTERNAS = 8
TAMANO_TABLERO = 600
MARGEN = 20
CELDA = 40

# Colores y configuraciones visuales
COLOR_FONDO = (240, 240, 240)
COLOR_TABLERO = (220, 220, 200)
# ... (otros colores)
````
Define las dimensiones del juego y constantes para el cálculo de posiciones.
   2. Clases del Juego
      Clase ```ficha```: Representa cada pieza del juego con su estado y posición
````python
class Ficha:
    def __init__(self, jugador, id_ficha):
        self.jugador = jugador
        self.id_ficha = id_ficha
        self.estado = "carcel"  # "carcel", posición externa o tupla ("interna", índice)
````

   Clase ```jugador```: Gestiona las fichas, contadores de dobles y movimientos extra
````python
class Jugador:
    def __init__(self, nombre, color, salida, entrada_hogar):
        self.nombre = nombre
        self.color = color
        self.salida = salida
        self.entrada_hogar = entrada_hogar
        self.fichas = [Ficha(self, i) for i in range(4)]
        # ... (otros atributos)
````
   3. Inicialización de Juego
````python
jugadores = [
    Jugador("Rojo", "red", salida=0, entrada_hogar=67),
    Jugador("Azul", "blue", salida=17, entrada_hogar=16),
    Jugador("Verde", "green", salida=34, entrada_hogar=33),
    Jugador("Amarillo", "yellow", salida=51, entrada_hogar=50),
]

posiciones_de_tablero = {i: [] for i in range(NUM_CASILLAS_EXTERNAS)}
casillas_seguras = {j.salida for j in jugadores}
````
Crea los cuatro jugadores con sus características únicas.
   
   4. Funciones de Lógica del Juego
   - Detección de bloqueos
````python
def es_bloqueo(pos):
    # Comprueba si hay dos fichas del mismo jugador en una casilla
````
   - Verificación de camino
````python
def verificar_camino(inicio, pasos):
    # Verifica que el camino esté libre de bloqueos
````
   - Movimiento de fichas
````python
def mover_ficha(ficha, pasos):
    # Implementa todas las reglas de movimiento:
    # - Salida de cárcel
    # - Movimiento normal
    # - Captura de fichas
    # - Entrada a vía interna
    # - Movimiento en vía interna
````
   5. Cálculo de Coordenadas
````python
# Coordenadas del tablero externo
coordenadas_del_tablero_externo = {}
# ... (cálculo de posiciones)

# Coordenadas de las vías internas
coordenadas_de_la_via_interna = {
    "Rojo": construir_coordenadas_de_la_via_interna_rojo(),
    # ... (otros jugadores)
}
````
Sistema para mapear posiciones lógicas a coordenadas gráficas en pantalla.
   6. Interfaz Gráfica con Pygame
````python
class InterfazParquesPygame:
    def __init__(self):
        # Inicialización de Pygame y configuración de ventana
    
    def dibujar_tablero(self):
        # Renderiza todos los elementos visuales
    
    def dibujar_dado(self, x, y, valor):
        # Dibuja un dado con el valor especificado
    
    def lanzar_dados(self):
        # Maneja la lógica de lanzamiento de dados
    
    def usar_dado(self, valor):
        # Aplica el movimiento con el valor del dado
    
    def terminar_turno(self):
        # Pasa al siguiente jugador
    
    def manejar_click(self, pos):
        # Gestiona los eventos de clic del ratón
    
    def ejecutar(self):
        # Bucle principal del juego
````

# Reglas del Juego Implementadas:
1. Para sacar una ficha de la cárcel se necesita un 5

2. Capturas: En casillas no seguras, envían la ficha contraria a la cárcel y otorgan 20 casillas bonus

3. Bloqueos: Dos fichas del mismo jugador bloquean el paso

4. Tres dobles consecutivos: Envían la última ficha movida a la cárcel

5. Exactitud: Requerida para entrar a la vía interna y para llegar a la meta

6. Movimientos extra: Otorgados por capturas y entradas a la vía interna

7. Victoria: Primer jugador en llevar todas sus fichas a la última casilla interna

