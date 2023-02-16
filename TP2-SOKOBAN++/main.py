import soko
import gamelib
import nivelesjuego
import controlesjuego

MULTIPLICADOR_TAMANIO_VENTANA = 64

def juego_crear():
    '''Inicializar el estado del juego.'''
    juego = {}
    juego['niveles'], juego['cant_niveles'] = nivelesjuego.inicializar_niveles("niveles.txt")
    juego['teclas'] = controlesjuego.definir_controles("teclas.txt")
    juego['nivel_actual'] = 0
    juego['grilla'] = soko.crear_grilla(juego['niveles'][juego['nivel_actual']])
    return juego

def juego_mostrar(grilla):
    '''Actualizar la ventana.'''
    for i in range(len(grilla)):
        for j in range(len(grilla[0])):
            #dibujo todo el terreno
            gamelib.draw_image('img\\ground.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)

            #agrego cada objeto encima
            if soko.hay_caja(grilla, j, i):
                gamelib.draw_image('img\\box.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_jugador(grilla, j, i):
                gamelib.draw_image('img\\player.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_pared(grilla, j, i):
                gamelib.draw_image('img\\wall.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)
            if soko.hay_objetivo(grilla, j, i):
                gamelib.draw_image('img\\goal.gif', j * MULTIPLICADOR_TAMANIO_VENTANA, i * MULTIPLICADOR_TAMANIO_VENTANA)

def juego_actualizar(juego, tecla):
    '''Actualizar el estado del juego.'''
    grilla = juego['grilla']
    nivel = juego['nivel_actual']
    movimiento = juego['teclas'][tecla]
    niveles = juego['niveles']
    ultimo_nivel = juego['cant_niveles']
    grilla = soko.mover(grilla, movimiento)
    if (soko.juego_ganado(grilla)) and (nivel != (ultimo_nivel - 1)):
        nivel += 1
        grilla = soko.crear_grilla(niveles[nivel])
        tamaño_horizontal, tamaño_vertical = soko.dimensiones(grilla)
        gamelib.resize(tamaño_horizontal * MULTIPLICADOR_TAMANIO_VENTANA, tamaño_vertical * MULTIPLICADOR_TAMANIO_VENTANA)
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
    except FileNotFoundError as e:
        print(e)
        return
    except IndexError as e:
        print(e)
        return
    tamaño_horizontal, tamaño_vertical = soko.dimensiones(juego['grilla'])
    gamelib.resize(tamaño_horizontal * MULTIPLICADOR_TAMANIO_VENTANA, tamaño_vertical * MULTIPLICADOR_TAMANIO_VENTANA)

    while gamelib.is_alive():
        gamelib.draw_begin()
        juego_mostrar(juego['grilla'])
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key

        if tecla == 'Escape':
            #El usuario presionó la tecla Escape, cerrar la aplicación.
            return

        elif tecla == 'r':
            #El usuario presionó la tecla r, se reinicia el nivel actual que está jugando.
            juego['grilla'] = soko.crear_grilla(juego['niveles'][juego['nivel_actual']])

        elif (tecla in juego['teclas']) and (tecla != 'r'):
            #El usuario presionó una tecla de los controles, se realiza el movimiento en cuestión.
            juego['grilla'], juego['nivel_actual'] = juego_actualizar(juego, tecla)
            if juego['nivel_actual'] == -1:
                return
            
gamelib.init(main)