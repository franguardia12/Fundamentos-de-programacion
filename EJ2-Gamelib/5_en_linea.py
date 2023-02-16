import gamelib

TAMANIO_VENTANA = 300
ANCHO_VENTANA = 300
ALTO_VENTANA = 300
DIM_GRILLA = 10
CANTIDAD_FILAS = 10
CANTIDAD_COLUMNAS = 10
SIMBOLO_X = 'X'
SIMBOLO_O = 'O'
CELDA_VACIA = ''
ANCHO_CELDA = (ANCHO_VENTANA // DIM_GRILLA)
ALTO_CELDA = (ALTO_VENTANA // DIM_GRILLA)
MITAD_CELDA = ANCHO_CELDA // 2

def juego_crear():
    """Inicializar el estado del juego"""
    return [[CELDA_VACIA for i in range(CANTIDAD_FILAS)] for j in range(CANTIDAD_COLUMNAS)]

def es_celda_vacia(grilla, i, j):
    '''Recibe dos coordenadas correspondiente a una posición en la grilla y la grilla de juego. Devuelve True si se encuentra vacía 
    dentro de los límites, false en caso contrario.'''
    if (i >= CANTIDAD_FILAS) or (j >= CANTIDAD_COLUMNAS): 
        return False
    return grilla[i][j] == CELDA_VACIA

def siguiente_turno(turno):
    '''Recibe el símbolo correspondiente a un turno y devuelve el siguiente turno.'''
    if turno == SIMBOLO_O:
        return SIMBOLO_X
    return SIMBOLO_O

def coordenadas_a_pixeles(i, j):
    '''Recibe dos coordenadas correspondientes a una posición en la grilla, devuelve el pasaje a coordenadas en píxeles 
    de la pantalla'''
    x = (j * ANCHO_CELDA) 
    y = (i * ALTO_CELDA) 
    return x, y

def pixeles_a_coordenadas(x, y):
    '''Recibe dos coordenadas correspondientes a una posición en píxeles de la pantalla, devuelve el pasaje a coordendas 
    de la grilla'''
    j = int(x // ANCHO_CELDA)
    i = int(y // ALTO_CELDA)
    return j, i

def juego_actualizar(juego, x, y, turno):
    """Actualizar el estado del juego

    x e y son las coordenadas (en pixels) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    coordenada_a, coordenada_b = pixeles_a_coordenadas(x, y)
    if es_celda_vacia(juego, coordenada_b, coordenada_a):
        juego[coordenada_b][coordenada_a] = turno
        turno = siguiente_turno(turno)
    return juego, turno

def juego_mostrar(juego, turno):
    """Actualizar la ventana"""
    #Dibujo el tablero
    gamelib.draw_text(f"Turno: {turno}", ANCHO_VENTANA // 2, ALTO_VENTANA + 20)
    gamelib.draw_rectangle(0, 0, ANCHO_VENTANA, ALTO_VENTANA, outline='white', fill='black')
    for i in range(0, TAMANIO_VENTANA, TAMANIO_VENTANA // DIM_GRILLA):
        gamelib.draw_line(0, i, ANCHO_VENTANA, i, fill='white', width=2)
        gamelib.draw_line(i, 0, i, ALTO_VENTANA, fill='white', width=2)

    for i in range(CANTIDAD_FILAS):
        for j in range(CANTIDAD_COLUMNAS):
            coordenada_x, coordenada_y = coordenadas_a_pixeles(i, j)
            gamelib.draw_text(juego[i][j], coordenada_x + MITAD_CELDA, coordenada_y + MITAD_CELDA, fill='white', anchor='c')

def main():
    gamelib.title("5 en línea")
    juego = juego_crear()
    turno = SIMBOLO_O

    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA + 50)

    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego, turno)
        gamelib.draw_end()

        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).

        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            juego, turno = juego_actualizar(juego, x, y, turno)

gamelib.init(main)