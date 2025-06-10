import random

# Inicializar tablero (68 casillas vacías)
tablero = [""] * 68

# Posiciones de salida por equipo
salidas = {"rojo": 5, "azul": 22, "verde": 39, "amarillo": 56}

# Fichas por equipo (cada ficha es [posicion, estado])
fichas = {
    "rojo": [["carcel", 0], ["carcel", 0], ["carcel", 0], ["carcel", 0]],
    "azul": [["carcel", 0], ["carcel", 0], ["carcel", 0], ["carcel", 0]],
}

def lanzar_dados():
    return random.randint(1, 6), random.randint(1, 6)

def dibujar_tablero():
    # Dibujo simplificado con casillas numeradas
    for i in range(68):
        print(f"[{i+1}: {tablero[i]}]", end=" ")
    print()

# Bucle principal (ejemplo)
turno = 0
equipos = ["rojo", "azul", "verde", "amarillo"]

while True:
    equipo_actual = equipos[turno % 4]
    dado1, dado2 = lanzar_dados()
    print(f"Turno de {equipo_actual}. Dados: {dado1}, {dado2}")
    
    # Lógica de movimiento aquí
    
    turno += 1