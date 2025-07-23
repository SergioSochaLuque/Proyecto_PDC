import pygame
import random
import sys
import math

# ---------------------
# PARAMETROS GLOBALES Y CONSTANTES
# ---------------------
NUM_CASILLAS_EXTERNAS = 68
NUM_CASILLAS_INTERNAS = 8
TAMANO_TABLERO = 600
MARGEN = 20
CELDA = 40

# Colores
COLOR_FONDO = (240, 240, 240)
COLOR_TABLERO = (220, 220, 200)
COLOR_TEXTO = (30, 30, 30)
COLOR_BOTON = (100, 150, 200)
COLOR_BOTON_HOVER = (120, 170, 220)
COLOR_DADO = (250, 250, 250)
COLOR_DADO_PUNTO = (30, 30, 30)
COLORES_JUGADORES = {
    "Rojo": (220, 60, 60),
    "Azul": (60, 100, 220),
    "Verde": (60, 160, 60),
    "Amarillo": (220, 180, 40)
}

# ---------------------
# CLASES DEL JUEGO: FICHA Y JUGADOR
# ---------------------
class Ficha:
    def __init__(self, jugador, id_ficha):
        self.jugador = jugador
        self.id_ficha = id_ficha
        self.estado = "carcel"
    
    def __str__(self):
        if self.estado == "carcel":
            return f"{self.jugador.nombre}{self.id_ficha}(carcel)"
        elif isinstance(self.estado, int):
            return f"{self.jugador.nombre}{self.id_ficha}(ext {self.estado})"
        elif isinstance(self.estado, tuple) and self.estado[0] == "interna":
            return f"{self.jugador.nombre}{self.id_ficha}(int {self.estado[1]})"
        return f"{self.jugador.nombre}{self.id_ficha}(?)"

class Jugador:
    def __init__(self, nombre, color, salida, entrada_hogar):
        self.nombre = nombre
        self.color = color
        self.salida = salida
        self.entrada_hogar = entrada_hogar
        self.fichas = [Ficha(self, i) for i in range(4)]
        self.contador_dobles = 0
        self.movimientos_extra = 0
        self.ultima_ficha_movida = None
    
    def todas_llegaron(self):
        for f in self.fichas:
            if not (isinstance(f.estado, tuple) and f.estado[0] == "interna" and f.estado[1] == (NUM_CASILLAS_INTERNAS - 1)):
                return False
        return True

# ---------------------
# CREACION DE JUGADORES
# ---------------------
jugadores = [
    Jugador("Rojo", "red", salida=0, entrada_hogar=67),
    Jugador("Azul", "blue", salida=17, entrada_hogar=16),
    Jugador("Verde", "green", salida=34, entrada_hogar=33),
    Jugador("Amarillo", "yellow", salida=51, entrada_hogar=50),
]

# ---------------------
# TABLERO EXTERNO Y CASILLAS SEGURAS
# ---------------------
posiciones_de_tablero = {i: [] for i in range(NUM_CASILLAS_EXTERNAS)}
casillas_seguras = {j.salida for j in jugadores}

# ---------------------
# FUNCIONES DE UTILIDAD
# ---------------------
def es_bloqueo(pos):
    if len(posiciones_de_tablero[pos]) == 2:
        f0, f1 = posiciones_de_tablero[pos]
        if f0.jugador == f1.jugador:
            return True
    return False

def verificar_camino(inicio, pasos):
    for i in range(1, pasos):
        pos_verificar = (inicio + i) % NUM_CASILLAS_EXTERNAS
        if es_bloqueo(pos_verificar):
            return False, pos_verificar
    return True, None

# ---------------------
# COORDENADAS PARA EL DIBUJO DEL TABLERO
# ---------------------
coordenadas_del_tablero_externo = {}
longitud_lado = 17
top_y = MARGEN
left_x = MARGEN
right_x = TAMANO_TABLERO - MARGEN
bottom_y = TAMANO_TABLERO - MARGEN

for i in range(longitud_lado):
    pos = i
    x = left_x + i * ((right_x - left_x) // (longitud_lado - 1))
    y = top_y
    coordenadas_del_tablero_externo[pos] = (x, y)
for i in range(longitud_lado):
    pos = 17 + i
    x = right_x
    y = top_y + i * ((bottom_y - top_y) // (longitud_lado - 1))
    coordenadas_del_tablero_externo[pos] = (x, y)
for i in range(longitud_lado):
    pos = 34 + i
    x = right_x - i * ((right_x - left_x) // (longitud_lado - 1))
    y = bottom_y
    coordenadas_del_tablero_externo[pos] = (x, y)
for i in range(longitud_lado):
    pos = 51 + i
    x = left_x
    y = bottom_y - i * ((bottom_y - top_y) // (longitud_lado - 1))
    coordenadas_del_tablero_externo[pos] = (x, y)

# Funciones para construir las vías internas
def construir_coordenadas_de_la_via_interna_rojo():
    coords = []
    centro_x = TAMANO_TABLERO // 2
    centro_y = TAMANO_TABLERO // 2
    for i in range(NUM_CASILLAS_INTERNAS):
        x = centro_x
        y = centro_y - (i + 1) * CELDA
        coords.append((x, y))
    return coords

def construir_coordenadas_de_la_via_interna_azul():
    coords = []
    centro_x = TAMANO_TABLERO // 2
    centro_y = TAMANO_TABLERO // 2
    for i in range(NUM_CASILLAS_INTERNAS):
        x = centro_x + (i + 1) * CELDA
        y = centro_y
        coords.append((x, y))
    return coords

def construir_coordenadas_de_la_via_interna_verde():
    coords = []
    centro_x = TAMANO_TABLERO // 2
    centro_y = TAMANO_TABLERO // 2
    for i in range(NUM_CASILLAS_INTERNAS):
        x = centro_x
        y = centro_y + (i + 1) * CELDA
        coords.append((x, y))
    return coords

def construir_coordenadas_de_la_via_interna_amarillo():
    coords = []
    centro_x = TAMANO_TABLERO // 2
    centro_y = TAMANO_TABLERO // 2
    for i in range(NUM_CASILLAS_INTERNAS):
        x = centro_x - (i + 1) * CELDA
        y = centro_y
        coords.append((x, y))
    return coords

coordenadas_de_la_via_interna = {
    "Rojo": construir_coordenadas_de_la_via_interna_rojo(),
    "Azul": construir_coordenadas_de_la_via_interna_azul(),
    "Verde": construir_coordenadas_de_la_via_interna_verde(),
    "Amarillo": construir_coordenadas_de_la_via_interna_amarillo(),
}

# Posiciones de la cárcel
posiciones_de_la_carcel = {
    "Rojo": {"x": 80, "y": 100, "offset_y": 25},
    "Azul": {"x": 500, "y": 100, "offset_y": 25},
    "Verde": {"x": 400, "y": 400, "offset_y": 25},
    "Amarillo": {"x": 150, "y": 400, "offset_y": 25},
}

# ---------------------
# LOGICA DE MOVIMIENTO
# ---------------------
def puede_colocar(ficha, pos):
    return (len(posiciones_de_tablero[pos]) < 2)

def mover_ficha(ficha, pasos):
    if ficha.estado == "carcel":
        if pasos != 5:
            return f"necesitas un 5 para sacar {ficha} de la carcel."
        if puede_colocar(ficha, ficha.jugador.salida):
            ficha.estado = ficha.jugador.salida
            posiciones_de_tablero[ficha.jugador.salida].append(ficha)
            ficha.jugador.ultima_ficha_movida = ficha
            return f"{ficha} sale de la carcel a la casilla {ficha.jugador.salida + 1}."
        else:
            return f"la salida de {ficha.jugador.nombre} esta bloqueada."
    
    if isinstance(ficha.estado, int):
        actual = ficha.estado
        hogar = ficha.jugador.entrada_hogar
        if hogar >= actual:
            d = hogar - actual
        else:
            d = (NUM_CASILLAS_EXTERNAS - actual) + hogar
        
        if pasos == d:
            valido, bloqueado = verificar_camino(actual, pasos)
            if not valido:
                return "movimiento no permitido: camino bloqueado por un bloqueo de dos fichas."
            if ficha in posiciones_de_tablero[actual]:
                posiciones_de_tablero[actual].remove(ficha)
            ficha.estado = ("interna", 0)
            ficha.jugador.movimientos_extra += 10
            ficha.jugador.ultima_ficha_movida = ficha
            return f"{ficha} entra a la via interna."
        elif pasos > d:
            return "movimiento no permitido: se requiere exactitud para entrar a la via interna."
        else:
            nuevo = (actual + pasos) % NUM_CASILLAS_EXTERNAS
            valido, bloqueado = verificar_camino(actual, pasos)
            if not valido:
                return "movimiento no permitido: camino bloqueado por un bloqueo de dos fichas."
            if posiciones_de_tablero[nuevo]:
                ocupante = posiciones_de_tablero[nuevo][0]
                if ocupante.jugador != ficha.jugador and nuevo not in casillas_seguras:
                    if ocupante in posiciones_de_tablero[nuevo]:
                        posiciones_de_tablero[nuevo].remove(ocupante)
                    ocupante.estado = "carcel"
                    if ficha in posiciones_de_tablero[actual]:
                        posiciones_de_tablero[actual].remove(ficha)
                    posiciones_de_tablero[nuevo].append(ficha)
                    ficha.estado = nuevo
                    bonus = 20
                    bonus_dest = (nuevo + bonus) % NUM_CASILLAS_EXTERNAS
                    valido_bonus, bloqueado_bonus = verificar_camino(nuevo, bonus)
                    if not valido_bonus:
                        return "movimiento bonus no permitido: camino bloqueado por un bloqueo de dos fichas."
                    if not puede_colocar(ficha, bonus_dest):
                        return "movimiento bonus no permitido: casilla destino bloqueada."
                    if ficha in posiciones_de_tablero[nuevo]:
                        posiciones_de_tablero[nuevo].remove(ficha)
                    posiciones_de_tablero[bonus_dest].append(ficha)
                    ficha.estado = bonus_dest
                    ficha.jugador.ultima_ficha_movida = ficha
                    return f"{ficha} captura a {ocupante} y se mueve 20 casillas adicionales a la casilla {bonus_dest + 1}."
            if ficha in posiciones_de_tablero[actual]:
                posiciones_de_tablero[actual].remove(ficha)
            posiciones_de_tablero[nuevo].append(ficha)
            ficha.estado = nuevo
            ficha.jugador.ultima_ficha_movida = ficha
            return f"{ficha} se mueve de la casilla {actual + 1} a {nuevo + 1}."
    
    if isinstance(ficha.estado, tuple) and ficha.estado[0] == "interna":
        indice = ficha.estado[1]
        nuevo_indice = indice + pasos
        if nuevo_indice >= NUM_CASILLAS_INTERNAS:
            return "movimiento no valido en la via interna (requiere exactitud)."
        ficha.estado = ("interna", nuevo_indice)
        ficha.jugador.ultima_ficha_movida = ficha
        if nuevo_indice == NUM_CASILLAS_INTERNAS - 1:
            ficha.jugador.movimientos_extra += 10
            return f"{ficha} ha llegado a la meta."
        return f"{ficha} avanza en la via interna a la casilla {nuevo_indice + 1}."
    
    return "movimiento desconocido."

# ---------------------
# INTERFAZ GRAFICA CON PYGAME
# ---------------------
class InterfazParquesPygame:
    def __init__(self):
        pygame.init()
        self.screen_width = TAMANO_TABLERO
        self.screen_height = TAMANO_TABLERO + 100  # Espacio adicional para controles
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Parques Tradicional")
        
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)
        self.dado_font = pygame.font.SysFont(None, 30)
        
        # Variables de estado
        self.indice_jugador_actual = 0
        self.valores_dados = []
        self.ficha_seleccionada = None
        self.ultimo_doble = False
        self.mensaje_estado = ""
        self.mensaje_turno = ""
        
        # Botones
        self.boton_lanzar = pygame.Rect(50, TAMANO_TABLERO + 20, 120, 40)
        self.boton_terminar = pygame.Rect(200, TAMANO_TABLERO + 20, 120, 40)
        
        self.actualizar_mensaje_turno()
        self.dibujar_tablero()
    
    def actualizar_mensaje_turno(self):
        actual = jugadores[self.indice_jugador_actual]
        self.mensaje_turno = f"Turno de: {actual.nombre} ({actual.color})"
    
    def dibujar_tablero(self):
        # Fondo
        self.screen.fill(COLOR_FONDO)
        
        # Dibujar el tablero
        pygame.draw.rect(self.screen, COLOR_TABLERO, 
                        (MARGEN, MARGEN, 
                         TAMANO_TABLERO - 2*MARGEN, 
                         TAMANO_TABLERO - 2*MARGEN))
        
        # Dibujar cuadrícula central
        centro = TAMANO_TABLERO // 2
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (centro, MARGEN), 
                        (centro, TAMANO_TABLERO - MARGEN), 2)
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (MARGEN, centro), 
                        (TAMANO_TABLERO - MARGEN, centro), 2)
        
        # Dibujar casillas externas
        for pos, (cx, cy) in coordenadas_del_tablero_externo.items():
            # Dibujar casilla
            rect = pygame.Rect(cx - 15, cy - 15, 30, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
            
            # Numerar casillas importantes
            num_casillas = pos + 1
            if num_casillas in [1, 18, 35, 52, 68]:
                texto = self.font.render(str(num_casillas), True, (0, 0, 0))
                self.screen.blit(texto, (cx - 5, cy - 8))
        
        # Dibujar vías internas
        for j in jugadores:
            lista_coords = coordenadas_de_la_via_interna[j.nombre]
            for i, (cx, cy) in enumerate(lista_coords):
                rect = pygame.Rect(cx - 15, cy - 15, 30, 30)
                pygame.draw.rect(self.screen, (240, 240, 240), rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                texto = self.font.render(str(i+1), True, (0, 0, 0))
                self.screen.blit(texto, (cx - 5, cy - 8))
        
        # Dibujar fichas en casillas externas
        for pos, fichas in posiciones_de_tablero.items():
            if fichas:
                cx, cy = coordenadas_del_tablero_externo[pos]
                for i, ficha in enumerate(fichas):
                    offset_x = i * 8 - 4
                    offset_y = i * 8 - 4
                    color = COLORES_JUGADORES[ficha.jugador.nombre]
                    pygame.draw.circle(self.screen, color, 
                                      (cx + offset_x, cy + offset_y), 10)
                    pygame.draw.circle(self.screen, (0, 0, 0), 
                                      (cx + offset_x, cy + offset_y), 10, 1)
                    
                    # Resaltar ficha seleccionada
                    if ficha == self.ficha_seleccionada:
                        pygame.draw.circle(self.screen, (255, 255, 255), 
                                          (cx + offset_x, cy + offset_y), 12, 2)
        
        # Dibujar fichas en la vía interna
        for j in jugadores:
            for ficha in j.fichas:
                if isinstance(ficha.estado, tuple) and ficha.estado[0] == "interna":
                    indice = ficha.estado[1]
                    cx, cy = coordenadas_de_la_via_interna[j.nombre][indice]
                    color = COLORES_JUGADORES[j.nombre]
                    pygame.draw.circle(self.screen, color, (cx, cy), 10)
                    pygame.draw.circle(self.screen, (0, 0, 0), (cx, cy), 10, 1)
                    
                    # Resaltar ficha seleccionada
                    if ficha == self.ficha_seleccionada:
                        pygame.draw.circle(self.screen, (255, 255, 255), 
                                          (cx, cy), 12, 2)
        
        # Dibujar fichas en la cárcel
        for j in jugadores:
            pos_carcel = posiciones_de_la_carcel[j.nombre]
            color = COLORES_JUGADORES[j.nombre]
            
            # Etiqueta de la cárcel
            texto = self.font.render(f"Cárcel {j.nombre}", True, color)
            self.screen.blit(texto, (pos_carcel["x"] - 30, pos_carcel["y"] - 30))
            
            cont = 0
            for ficha in j.fichas:
                if ficha.estado == "carcel":
                    px = pos_carcel["x"]
                    py = pos_carcel["y"] + cont * pos_carcel["offset_y"]
                    cont += 1
                    
                    # Dibujar triángulo para fichas en cárcel
                    puntos = [
                        (px, py - 10),
                        (px - 10, py + 10),
                        (px + 10, py + 10)
                    ]
                    pygame.draw.polygon(self.screen, color, puntos)
                    pygame.draw.polygon(self.screen, (0, 0, 0), puntos, 1)
                    
                    # Resaltar ficha seleccionada
                    if ficha == self.ficha_seleccionada:
                        pygame.draw.polygon(self.screen, (255, 255, 255), [
                            (px, py - 12),
                            (px - 12, py + 12),
                            (px + 12, py + 12)
                        ], 2)
        
        # Dibujar panel de control
        pygame.draw.rect(self.screen, (230, 230, 230), 
                        (0, TAMANO_TABLERO, 
                         self.screen_width, 100))
        pygame.draw.line(self.screen, (150, 150, 150), 
                        (0, TAMANO_TABLERO), 
                        (self.screen_width, TAMANO_TABLERO), 2)
        
        # Botón Lanzar dados
        boton_color = COLOR_BOTON_HOVER if self.boton_lanzar.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
        pygame.draw.rect(self.screen, boton_color, self.boton_lanzar, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), self.boton_lanzar, 2, border_radius=5)
        texto = self.font.render("Lanzar dados", True, (255, 255, 255))
        self.screen.blit(texto, (self.boton_lanzar.centerx - texto.get_width()//2, 
                                self.boton_lanzar.centery - texto.get_height()//2))
        
        # Botón Terminar turno
        boton_color = COLOR_BOTON_HOVER if self.boton_terminar.collidepoint(pygame.mouse.get_pos()) else COLOR_BOTON
        pygame.draw.rect(self.screen, boton_color, self.boton_terminar, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), self.boton_terminar, 2, border_radius=5)
        texto = self.font.render("Terminar turno", True, (255, 255, 255))
        self.screen.blit(texto, (self.boton_terminar.centerx - texto.get_width()//2, 
                                self.boton_terminar.centery - texto.get_height()//2))
        
        # Información de turno
        texto = self.title_font.render(self.mensaje_turno, True, COLORES_JUGADORES[jugadores[self.indice_jugador_actual].nombre])
        self.screen.blit(texto, (400, TAMANO_TABLERO + 15))
        
        # Mensaje de estado
        if self.mensaje_estado:
            texto = self.font.render(self.mensaje_estado, True, (200, 0, 0))
            self.screen.blit(texto, (50, TAMANO_TABLERO + 70))
        
        # Mostrar dados lanzados
        if self.valores_dados:
            for i, valor in enumerate(self.valores_dados):
                self.dibujar_dado(500 + i*60, TAMANO_TABLERO + 30, valor)
        
        pygame.display.flip()
    
    def dibujar_dado(self, x, y, valor):
        # Dibujar el dado
        dado_rect = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(self.screen, COLOR_DADO, dado_rect, border_radius=5)
        pygame.draw.rect(self.screen, (0, 0, 0), dado_rect, 2, border_radius=5)
        
        # Dibujar puntos según el valor
        radio = 4
        if valor == 1:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 20, y + 20), radio)
        elif valor == 2:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 28), radio)
        elif valor == 3:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 20, y + 20), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 28), radio)
        elif valor == 4:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 28), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 28), radio)
        elif valor == 5:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 12), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 20, y + 20), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 28), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 28), radio)
        elif valor == 6:
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 10), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 10), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 20), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 20), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 12, y + 30), radio)
            pygame.draw.circle(self.screen, COLOR_DADO_PUNTO, (x + 28, y + 30), radio)
    
    def lanzar_dados(self):
        actual = jugadores[self.indice_jugador_actual]
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.ultimo_doble = (d1 == d2)
        if d1 == d2:
            actual.contador_dobles += 1
        else:
            actual.contador_dobles = 0

        # Regla de tres dobles consecutivos
        if actual.contador_dobles == 3:
            if actual.ultima_ficha_movida is None:
                if self.ficha_seleccionada is not None:
                    actual.ultima_ficha_movida = self.ficha_seleccionada
                else:
                    for f in actual.fichas:
                        if f.estado != "carcel":
                            actual.ultima_ficha_movida = f
                            break
                    if actual.ultima_ficha_movida is None:
                        actual.ultima_ficha_movida = actual.fichas[0]
            ficha_a_carcel = actual.ultima_ficha_movida
            if isinstance(ficha_a_carcel.estado, int):
                pos = ficha_a_carcel.estado
                if ficha_a_carcel in posiciones_de_tablero[pos]:
                    posiciones_de_tablero[pos].remove(ficha_a_carcel)
            ficha_a_carcel.estado = "carcel"
            self.mensaje_estado = "Tres dobles consecutivos: la ficha " + str(ficha_a_carcel) + " regresa a la cárcel."
            actual.contador_dobles = 0
            return

        self.valores_dados = [d1, d2]
        self.mensaje_estado = "Selecciona una ficha y luego un dado para mover"
    
    def usar_dado(self, valor):
        if self.ficha_seleccionada is None:
            self.mensaje_estado = "Primero selecciona una ficha."
            return
        
        resultado = mover_ficha(self.ficha_seleccionada, valor)
        jugadores[self.indice_jugador_actual].ultima_ficha_movida = self.ficha_seleccionada
        self.valores_dados.remove(valor)
        self.ficha_seleccionada = None
        self.mensaje_estado = resultado
        
        if not self.valores_dados:
            self.terminar_turno()
    
    def terminar_turno(self):
        self.valores_dados = []
        self.ficha_seleccionada = None
        actual = jugadores[self.indice_jugador_actual]
        
        if not self.ultimo_doble:
            actual.contador_dobles = 0
            self.indice_jugador_actual = (self.indice_jugador_actual + 1) % len(jugadores)
            self.actualizar_mensaje_turno()
        else:
            self.ultimo_doble = False
        
        self.mensaje_estado = ""
    
    def manejar_click(self, pos):
        x, y = pos
        
        # Verificar clic en botones
        if self.boton_lanzar.collidepoint(x, y):
            self.lanzar_dados()
            return
        elif self.boton_terminar.collidepoint(x, y):
            self.terminar_turno()
            return
        
        # Verificar clic en dados
        if y > TAMANO_TABLERO:
            if self.valores_dados:
                for i, valor in enumerate(self.valores_dados):
                    dado_rect = pygame.Rect(500 + i*60, TAMANO_TABLERO + 30, 40, 40)
                    if dado_rect.collidepoint(x, y):
                        self.usar_dado(valor)
                        return
        
        # Verificar clic en el tablero
        if y < TAMANO_TABLERO:
            actual = jugadores[self.indice_jugador_actual]
            ficha_click = None
            
            # Buscar en casillas externas
            for pos_tablero, (cx, cy) in coordenadas_del_tablero_externo.items():
                if abs(x - cx) < 15 and abs(y - cy) < 15:
                    if posiciones_de_tablero[pos_tablero]:
                        for f in posiciones_de_tablero[pos_tablero]:
                            if f.jugador == actual:
                                ficha_click = f
                                break
                if ficha_click:
                    break
            
            # Buscar en vías internas
            if not ficha_click:
                lista_coords = coordenadas_de_la_via_interna[actual.nombre]
                for idx, (cx, cy) in enumerate(lista_coords):
                    if abs(x - cx) < 15 and abs(y - cy) < 15:
                        for f in actual.fichas:
                            if f.estado == ("interna", idx):
                                ficha_click = f
                                break
                    if ficha_click:
                        break
            
            # Buscar en la cárcel
            if not ficha_click:
                for j in jugadores:
                    info_carcel = posiciones_de_la_carcel[j.nombre]
                    x_carcel = info_carcel["x"]
                    y_carcel = info_carcel["y"]
                    offset = info_carcel["offset_y"]
                    cont = 0
                    for f in j.fichas:
                        if f.estado == "carcel":
                            py = y_carcel + cont * offset
                            cont += 1
                            
                            # Verificar si el clic está dentro del triángulo
                            distancia = math.sqrt((x - x_carcel)**2 + (y - py)**2)
                            if distancia < 15 and f.jugador == actual:
                                ficha_click = f
                                break
                    if ficha_click:
                        break
            
            if ficha_click:
                self.ficha_seleccionada = ficha_click
                self.mensaje_estado = f"Seleccionada {ficha_click}"
    
    def ejecutar(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic izquierdo
                        self.manejar_click(event.pos)
            
            self.dibujar_tablero()
            clock.tick(30)
        
        pygame.quit()
        sys.exit()

# ---------------------
# EJECUCION DEL JUEGO
# ---------------------
def main():
    juego = InterfazParquesPygame()
    juego.ejecutar()

if __name__ == "__main__":
    main()