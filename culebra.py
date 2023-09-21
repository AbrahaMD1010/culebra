from collections import deque
from random import randrange

import pygame

WINDOWS = 780
TILE_SIZE = 60
RANGE = (1, (WINDOWS // TILE_SIZE) + 1)
screen = pygame.display.set_mode([WINDOWS] * 2)

mapa = {(posx, posy): [i, j] for posx, i in enumerate(range(0, WINDOWS, TILE_SIZE), start=1) for posy, j in
        enumerate(range(0, WINDOWS, TILE_SIZE), start=1)}

pygame.init()

# culebra
cuerpo_culebra = deque([mapa[(5, 5)], mapa[(4, 5)], mapa[(3, 5)]])
culebra_direccion = "arriba"

# manzana
manzana_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
manzana_surf.fill("red")
manzana_rect = manzana_surf.get_rect()
manzana_posicion = [randrange(*RANGE), randrange(*RANGE)]
manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]

# #####################

nuevo_y: int = cuerpo_culebra[1][1]
nuevo_x: int = cuerpo_culebra[1][0]

estado_juego = False

clock = pygame.time.Clock()

while True:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:
            estado_juego = True
            if event.key == pygame.K_UP and culebra_direccion != "abajo":
                culebra_direccion = 'arriba'
            elif event.key == pygame.K_DOWN and culebra_direccion != "arriba":
                culebra_direccion = 'abajo'
            elif event.key == pygame.K_LEFT and culebra_direccion != "derecha":
                culebra_direccion = 'izquierda'
            elif event.key == pygame.K_RIGHT and culebra_direccion != "izquierda":
                culebra_direccion = 'derecha'
    if estado_juego:
        screen.fill("black")
        for i in range(0, WINDOWS, TILE_SIZE):
            for j in range(0, WINDOWS, TILE_SIZE):
                pygame.draw.rect(screen, 'white', (i, j, TILE_SIZE, TILE_SIZE), 1)

        if culebra_direccion == "arriba":
            nuevo_y -= TILE_SIZE
        if culebra_direccion == "abajo":
            nuevo_y += TILE_SIZE
        if culebra_direccion == "izquierda":
            nuevo_x -= TILE_SIZE
        if culebra_direccion == "derecha":
            nuevo_x += TILE_SIZE

        cuerpo_culebra.appendleft([nuevo_x, nuevo_y])
        # print(cuerpo_culebra, manzana_rect.topleft)
        if tuple(cuerpo_culebra[0]) == manzana_rect.topleft:
            # puntos +1
            manzana_posicion = [randrange(*RANGE), randrange(*RANGE)]
            manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]
            pass
        else:
            cuerpo_culebra.pop()

        # verificar choques
        if (cuerpo_culebra[0][0] < 0 or cuerpo_culebra[0][1] < 0
                or cuerpo_culebra[0][0] > WINDOWS or cuerpo_culebra[0][1] > WINDOWS):

            estado_juego = False

        if cuerpo_culebra[0] in list(cuerpo_culebra)[1:]:
            estado_juego = False
        # ##

        for parte in cuerpo_culebra:
            # print(parte[0], parte[1])
            rect = pygame.Rect(parte[0], parte[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, "green", rect)

        screen.blit(manzana_surf, manzana_rect)
    else:
        cuerpo_culebra = deque([mapa[(7, 9)], mapa[(7, 8)], mapa[(7, 7)]])
        culebra_direccion = "arriba"

        # manzana

        manzana_posicion = [randrange(*RANGE), randrange(*RANGE)]
        manzana_rect.topleft = mapa[manzana_posicion[0], manzana_posicion[1]]

        # #####################

        nuevo_y: int = cuerpo_culebra[1][1]
        nuevo_x: int = cuerpo_culebra[1][0]

        screen.fill("black")
        for parte in cuerpo_culebra:
            # print(parte[0], parte[1])
            rect = pygame.Rect(parte[0], parte[1], TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, "green", rect)

        for i in range(0, WINDOWS, TILE_SIZE):
            for j in range(0, WINDOWS, TILE_SIZE):
                pygame.draw.rect(screen, 'white', (i, j, TILE_SIZE, TILE_SIZE), 1)

        estado_juego = False

    pygame.display.flip()


#te amo alejo