import soko
import gamelib
import inicializarjuego
import logica
from pila import Pila
from cola import Cola

MULTIPLICADOR_TAMANIO_VENTANA = 64
NIVELES = 'niveles'
CANT_NIVELES = 'cant_niveles'
TECLAS = 'teclas'
NIVEL_ACTUAL = 'nivel_actual'
GRILLA = 'grilla'
DESHACER = 'deshacer'
REHACER = 'rehacer'
PISTAS = 'pistas'

def juego_crear():
    '''Inicializar el estado del juego.'''
    juego = {}
    juego[NIVELES], juego[CANT_NIVELES] = inicializarjuego.inicializar_niveles("niveles.txt")
    juego[TECLAS] = inicializarjuego.definir_controles("teclas.txt")
    juego[NIVEL_ACTUAL] = 0
    juego[GRILLA] = soko.crear_grilla(juego[NIVELES][juego[NIVEL_ACTUAL]])
    juego[DESHACER] = Pila()
    juego[REHACER] = Pila()
    juego[PISTAS] = Cola()
    return juego

def juego_mostrar(juego):
    '''Actualizar la ventana.'''
    if not juego[PISTAS].esta_vacia():
        tamaño_x, tamaño_y = soko.dimensiones(juego[GRILLA])
        gamelib.draw_text('Pista disponible', tamaño_x * MULTIPLICADOR_TAMANIO_VENTANA / 2, tamaño_y * MULTIPLICADOR_TAMANIO_VENTANA + 10)
    for i in range(len(juego[GRILLA])):
        for j in range(len(juego[GRILLA][0])):
            #dibujo todo el terreno
            gamelib.draw_image('img\\ground.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)

            #agrego cada objeto encima
            if soko.hay_caja(juego[GRILLA], j, i):
                gamelib.draw_image('img\\box.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_jugador(juego[GRILLA], j, i):
                gamelib.draw_image('img\\player.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_pared(juego[GRILLA], j, i):
                gamelib.draw_image('img\\wall.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_objetivo(juego[GRILLA], j, i):
                gamelib.draw_image('img\\goal.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)

def juego_actualizar(juego, tecla):
    '''Actualizar el estado del juego.'''
    if tecla == 'p':
        movimiento = juego[PISTAS].desencolar()
    else:
        movimiento = juego[TECLAS][tecla]
    grilla = juego[GRILLA]
    nivel = juego[NIVEL_ACTUAL]
    niveles = juego[NIVELES]
    ultimo_nivel = juego[CANT_NIVELES]
    juego[DESHACER].apilar(grilla)
    grilla = soko.mover(grilla, movimiento)
    if (soko.juego_ganado(grilla)) and (nivel != (ultimo_nivel - 1)):
        nivel += 1
        grilla = soko.crear_grilla(niveles[nivel])
        tamaño_horizontal, tamaño_vertical = soko.dimensiones(grilla)
        gamelib.resize(tamaño_horizontal * MULTIPLICADOR_TAMANIO_VENTANA, tamaño_vertical * MULTIPLICADOR_TAMANIO_VENTANA + 20)
        logica.resetear_estados(juego)
    elif (soko.juego_ganado(grilla)) and (nivel == (ultimo_nivel - 1)):
        gamelib.draw_begin()
        gamelib.say("Ganaste el juego! :) ")
        gamelib.draw_end()
        nivel = -1
    return grilla, nivel
    
def main():
    gamelib.title("Sokoban")
    try:
        juego = juego_crear()
    except FileNotFoundError:
        return
    except IndexError:
        return
    tamaño_horizontal, tamaño_vertical = soko.dimensiones(juego[GRILLA])
    gamelib.resize(tamaño_horizontal * MULTIPLICADOR_TAMANIO_VENTANA, tamaño_vertical * MULTIPLICADOR_TAMANIO_VENTANA + 20)

    while gamelib.is_alive():
        gamelib.draw_begin()
        juego_mostrar(juego)
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key

        if tecla == 'Escape':
            #El usuario presionó la tecla Escape, cerrar la aplicación.
            return

        if tecla == 'r':
            #El usuario presionó la tecla r, se reinicia el nivel actual que está jugando.
            juego[GRILLA] = soko.crear_grilla(juego[NIVELES][juego[NIVEL_ACTUAL]])
            logica.resetear_estados(juego)
            continue

        if tecla == 'z':
            #El usuario presionó la tecla z, se deshace el último movimiento hecho.
            logica.deshacer_movimiento(juego)
            continue

        if tecla == 'x':
            #El usuario presionó la tecla x, se rehace el último movimiento deshecho.
            logica.rehacer_movimiento(juego)
            continue

        if tecla == 'p':
            #El usuario presionó la tecla p, se ejecuta la pista disponible.
            if juego[PISTAS].esta_vacia():
                logica.buscar_pistas(juego)
            else:
                while not juego[REHACER].esta_vacia():
                    juego[REHACER].desapilar()
                juego[GRILLA], juego[NIVEL_ACTUAL] = juego_actualizar(juego, tecla)
                if juego[NIVEL_ACTUAL] == -1:
                    return
            continue

        if tecla in juego[TECLAS]:
            #El usuario presionó una tecla de los controles, se realiza el movimiento en cuestión.
            while not juego[REHACER].esta_vacia():
                juego[REHACER].desapilar()
            while not juego[PISTAS].esta_vacia():
                juego[PISTAS].desencolar()
            juego[GRILLA], juego[NIVEL_ACTUAL] = juego_actualizar(juego, tecla)
            if juego[NIVEL_ACTUAL] == -1:
                return
            
gamelib.init(main)