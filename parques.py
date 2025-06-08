import random
tablero = [""] * 68  
jugadores = ["Rojo", "Azul"]
posiciones = [0, 0] 
def lanzar_dado():
    return random.randint(1, 6)
turno = 0
while True:
    print(f"\nTurno de {jugadores[turno]}")
    input("Presiona Enter para lanzar el dado...")
    dado = lanzar_dado()
    print(f"Salió un {dado}")
    posiciones[turno] = (posiciones[turno] + dado) % len(tablero)
    print(f"{jugadores[turno]} está en la casilla {posiciones[turno]}")
    
    # Condición de victoria simple (puedes mejorarla)
    if posiciones[turno] == len(tablero) - 1:
        print(f"¡{jugadores[turno]} ha ganado!")
        break
    
    # Cambiar de turno
    turno = (turno + 1) % len(jugadores)