# inicializar_tablero.py
def inicializar_tablero():
    # Lista de 68 posiciones del recorrido principal
    recorrido = list(range(68))
    # Diccionarios para casas y metas
    casas = {color: [] for color in ['rojo','verde','amarillo','azul']}
    metas = {color: [] for color in ['rojo','verde','amarillo','azul']}
    return recorrido, casas, metas

# dado.py
import random

def tirar_dado():
    return random.randint(1,6)

# movimiento.py

def mover_ficha(pos_actual, pasos, recorrido):
    nueva_pos = pos_actual + pasos
    if nueva_pos < len(recorrido):
        return nueva_pos
    else:
        # lógica de llegada a meta (pendiente)
        return None