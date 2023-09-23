import time
from collections import deque
from random import randrange, randint

import pygame
from pygame.event import Event

pygame.init()

WINDOWS = 780
CUADRADO_SIZE = 60
RANGE = (1, (WINDOWS // CUADRADO_SIZE) + 1)
screen = pygame.display.set_mode([WINDOWS] * 2)

mapa = {(posx, posy): [i, j] for posx, i in enumerate(range(0, WINDOWS, CUADRADO_SIZE), start=1) for posy, j in
        enumerate(range(0, WINDOWS, CUADRADO_SIZE), start=1)}

# culebra
cuerpo_culebra = deque([mapa[(6, 6)], mapa[(6, 7)], mapa[(6, 8)]])

culebra_direccion = "arriba"

# manzana
manzana_surf = pygame.Surface((CUADRADO_SIZE, CUADRADO_SIZE))
manzana_surf.fill("red")
manzana_rect = manzana_surf.get_rect()
manzana_posicion = [9, 3]
manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]
tiempo_espera_manzana = 0  # tiempo entre que come una manzanay aparece otra

# #####################

nuevo_y: int = cuerpo_culebra[0][1]
nuevo_x: int = cuerpo_culebra[0][0]

estado_juego = False
bloqueado_input = False

clock = pygame.time.Clock()
# puntos = 0
while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            estado_juego = True
            if not bloqueado_input:
                bloqueado_input = True
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and culebra_direccion != "abajo":
                    culebra_direccion = 'arriba'
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and culebra_direccion != "arriba":
                    culebra_direccion = 'abajo'
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and culebra_direccion != "derecha":
                    culebra_direccion = 'izquierda'
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and culebra_direccion != "izquierda":
                    culebra_direccion = 'derecha'

    if estado_juego:
        screen.fill("black")

        if len(cuerpo_culebra) == ((WINDOWS//CUADRADO_SIZE)**2)-1:
            estado_juego = False
            victoria_fuente = pygame.font.SysFont("verdana", 30)
            texto_victoria_surf = victoria_fuente.render("GANASTE!!", True, "red")
            texto_victoria_rect = texto_victoria_surf.get_rect()
            texto_victoria_rect.center = (WINDOWS//2, WINDOWS//2)
            screen.blit(texto_victoria_surf, texto_victoria_rect)
            time.sleep(3)
            continue

        for i in range(0, WINDOWS, CUADRADO_SIZE):
            for j in range(0, WINDOWS, CUADRADO_SIZE):
                pygame.draw.rect(screen, 'white', (i, j, CUADRADO_SIZE, CUADRADO_SIZE), 1)

        if culebra_direccion == "arriba":
            nuevo_y -= CUADRADO_SIZE
        if culebra_direccion == "abajo":
            nuevo_y += CUADRADO_SIZE
        if culebra_direccion == "izquierda":
            nuevo_x -= CUADRADO_SIZE
        if culebra_direccion == "derecha":
            nuevo_x += CUADRADO_SIZE

        cuerpo_culebra.appendleft([nuevo_x, nuevo_y])
        if tuple(cuerpo_culebra[0]) == manzana_rect.topleft:  # si se come la manzana
            puntos += 1
            tiempo_espera_manzana = randint(1, 10)
            manzana_posicion = [randrange(*RANGE), randrange(*RANGE)]
            while mapa[manzana_posicion[0], manzana_posicion[1]] in cuerpo_culebra:
                manzana_posicion = [randrange(*RANGE), randrange(*RANGE)]
            manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]
        else:
            cuerpo_culebra.pop()

        # verificar choques
        if (cuerpo_culebra[0][0] < 0 or cuerpo_culebra[0][1] < 0
                or cuerpo_culebra[0][0] > WINDOWS - CUADRADO_SIZE or cuerpo_culebra[0][1] > WINDOWS - CUADRADO_SIZE):
            estado_juego = False

        if cuerpo_culebra[0] in list(cuerpo_culebra)[1:]:
            estado_juego = False

        # dibujer culebra
        cabeza = True
        for parte in cuerpo_culebra:
            if not cabeza:
                rect = pygame.Rect(parte[0], parte[1], CUADRADO_SIZE, CUADRADO_SIZE)
                pygame.draw.rect(screen, "green", rect)
            else:
                rect = pygame.Rect(parte[0], parte[1], CUADRADO_SIZE, CUADRADO_SIZE)
                pygame.draw.rect(screen, "white", rect)
                cabeza = False
        # ##

        # dibujar manzana
        if tiempo_espera_manzana == 0:
            screen.blit(manzana_surf, manzana_rect)
        else:
            screen.blit(manzana_surf, (800, 800))
            tiempo_espera_manzana -= 1 if tiempo_espera_manzana > 0 else 0
        bloqueado_input = False

        # texto puntos
        texto_fuente = pygame.font.SysFont("verdana", 30)
        texto_surf = texto_fuente.render(f"Puntos: {puntos}", True, "white")
        texto_rect = texto_surf.get_rect()
        screen.blit(texto_surf, texto_rect)

    else:
        puntos = 0
        texto_fuente = pygame.font.SysFont("verdana", 30)
        texto_surf = texto_fuente.render("Puntos: 0", True, "white")
        texto_rect = texto_surf.get_rect()
        texto_rect.topleft = (0, 0)

        instrucciones = texto_fuente.render("Mover: WASD o flechas", True, "black", "orange")
        instrucciones_rect = instrucciones.get_rect()
        instrucciones_rect.center = (WINDOWS//2, WINDOWS//2)

        cuerpo_culebra = deque([mapa[(7, 7)], mapa[(7, 8)], mapa[(7, 9)]])
        culebra_direccion = "arriba"
        # manzana

        manzana_posicion = [10, 3]
        manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]

        # #####################

        nuevo_y: int = cuerpo_culebra[0][1]
        nuevo_x: int = cuerpo_culebra[0][0]

        screen.fill("black")
        cabeza = True
        for parte in cuerpo_culebra:
            if not cabeza:
                rect = pygame.Rect(parte[0], parte[1], CUADRADO_SIZE, CUADRADO_SIZE)
                pygame.draw.rect(screen, "green", rect)

            else:
                rect = pygame.Rect(parte[0], parte[1], CUADRADO_SIZE, CUADRADO_SIZE)
                pygame.draw.rect(screen, "white", rect)
                cabeza = False

        for i in range(0, WINDOWS, CUADRADO_SIZE):
            for j in range(0, WINDOWS, CUADRADO_SIZE):
                pygame.draw.rect(screen, 'white', (i, j, CUADRADO_SIZE, CUADRADO_SIZE), 1)

        screen.blit(manzana_surf, manzana_rect)
        screen.blit(texto_surf, texto_rect)
        screen.blit(instrucciones, instrucciones_rect)

    pygame.display.flip()

