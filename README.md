# Descripción
Este proyecto es una implementación del juego de mesa "Parques Tradicional" utilizando Python y la biblioteca Tkinter para la interfaz gráfica. El juego sigue las reglas clásicas del parqués con cuatro jugadores (Rojo, Azul, Verde y Amarillo), donde cada jugador debe mover sus cuatro fichas desde la cárcel hasta la meta, pasando por un tablero exterior y una vía interna.
# Características
- Tablero clásico con 68 casillas externas y 8 casillas internas por jugador
- Sistema de turnos con lanzamiento de dados**
- Mecánicas de juego completas:
    * Sacar fichas de la cárcel con 5
    * Captura de fichas enemigas
    * Movimientos bonus por capturas y entradas a la vía interna
    * Bloqueos con dos fichas del mismo color
    * Penalización por tres dobles consecutivos
    * Requisito de exactitud para entrar a la vía interna y meta}
- Interfaz gráfica intuitiva con representación visual del tablero
- Sistema de selección de fichas mediante clics
# Requisitos
- Python 3.6 o superior
- Biblioteca Tkinter (normalmente incluida en instalaciones estándar de Python)
# Instrucciones de Ejecución
1. Clona el repositorio o descarga el archivo ```parques.py```
2. Ejecuta el siguiente comando en tu terminal:
````python
python parques.py
````
# Controles del Juego
1. Lanzar dados: Haz clic en el botón "Lanzar dados" para comenzar tu turno
2. Seleccionar ficha: Haz clic en cualquiera de tus fichas (en cárcel, tablero externo o vía interna)
3. Usar dado: Selecciona un valor de dado para mover tu ficha seleccionada
4. Terminar turno: Pasa al siguiente jugador cuando hayas usado todos tus dados
# Estructura del Código:
El código está organizado en las siguientes secciones principales:
   1. Parámetros Globales y Constantes
````python
NUM_CASILLAS_EXTERNAS = 68
NUM_CASILLAS_INTERNAS = 8
TAMANO_TABLERO = 600
MARGEN = 20
CELDA = 40
````
Define las dimensiones del juego y constantes para el cálculo de posiciones.
   2. Clases del Juego
      Clase ```ficha```: Representa cada pieza del juego con su estado y posición
      Clase ```jugador```: Gestiona las fichas, contadores de dobles y movimientos extra
   3. Inicialización de Jugadores
````python
jugadores = [
    Jugador("Rojo", "red", salida=0, entrada_hogar=67),
    Jugador("Azul", "blue", salida=17, entrada_hogar=16),
    ...
]
````
Crea los cuatro jugadores con sus características únicas.
   4. Sistema de Posiciones
      ```posiciones_de_tablero```: Diccionario que rastrea fichas en cada casilla
      ```casillas_seguras```: Casillas donde no se pueden capturar fichas
   5. Funciones de Lógica del Juego
      ```s_bloqueo()```: Detecta bloqueos de dos fichas del mismo color
      ```verificar_camino()```: Comprueba si el camino entre casillas está libre
      ```mover_ficha()```: Implementa todas las reglas de movimiento
   6. Cálculo de Coordenadas
      -Sistema para mapear posiciones lógicas a coordenadas gráficas
      -Funciones específicas para tablero externo y vías internas
   7. Interfaz Gráfica (```InterfazParques```)
      -```dibujar_tablero()```: Renderiza todos los elementos visuales
      -```lanzar_dados()```: Maneja la lógica de lanzamiento
      -```al_hacer_click_en_canvas()```: Detecta interacciones del jugador
