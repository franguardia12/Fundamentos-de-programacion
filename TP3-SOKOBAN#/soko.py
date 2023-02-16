PARED = '#'
CAJA = '$'
JUGADOR = '@'
OBJETIVO = '.'
OBJETIVO_CON_CAJA = '*'
OBJETIVO_CON_JUGADOR = '+'
ESPACIO_VACIO = ' '

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    '''
    grilla = []
    for i in range(len(desc)):
        grilla.append([])
        for j in range(len(desc[0])):
            grilla[i].append(desc[i][j])
    return grilla

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    col = 0
    fil = 0
    (col, fil) = (len(grilla[0]), len(grilla))
    return (col, fil)

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return (grilla[f][c] == OBJETIVO) or (grilla[f][c] == OBJETIVO_CON_CAJA) or (grilla[f][c] == OBJETIVO_CON_JUGADOR)

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return (grilla[f][c] == CAJA) or (grilla[f][c] == OBJETIVO_CON_CAJA)

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return (grilla[f][c] == JUGADOR) or (grilla[f][c] == OBJETIVO_CON_JUGADOR)

def hay_espacio_vacio(grilla, c, f):
    '''Devuelve True si hay un espacio vacío en la columna y fila (c, f).'''
    return grilla[f][c] == ESPACIO_VACIO

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in grilla:
        for celda in fila:
            if celda == CAJA: return False
    return True

def copiar_grilla(grilla):
    '''Recibe la grilla armada y realiza una copia profunda de ella en una nueva grilla'''
    nueva_grilla = []
    for i in range(len(grilla)):
        nueva_grilla.append([])
        for j in range(len(grilla[0])):
            nueva_grilla[i].append(grilla[i][j])
    return nueva_grilla

def es_celda_vacia_para_caja(grilla, direccion):
    '''Recibe la grilla armada y alguna de las coordenadas de la posición válidas, devuelve True si la celda a la que se quiere
     mover la caja está libre o no, es decir que no haya una pared u otra caja. False en caso contrario'''
    (x_direccion, y_direccion) = direccion
    celda = grilla[x_direccion][y_direccion]
    if hay_pared(grilla, y_direccion, x_direccion) or hay_caja(grilla, y_direccion, x_direccion): 
        return False
    return True

def es_celda_vacia(grilla, direccion1, direccion2):
    '''Recibe la grilla armada y dos coordenadas de posición válidas, devuelve True si la celda a la que se quiere mover el jugador
    está libre o no, es decir que no haya una pared u otra caja. False en caso contrario'''
    (x_direccion1, y_direccion1) = direccion1
    if hay_pared(grilla, y_direccion1, x_direccion1): 
        return False
    elif hay_caja(grilla, y_direccion1, x_direccion1):
        if not es_celda_vacia_para_caja(grilla, direccion2):
             return False
    return True

def buscar_jugador(grilla):
    '''Recibe la grilla armada y devuelve la posición del jugador en forma de lista de dos números'''
    posicion = [0, 0]
    for f in range(len(grilla)):
        for c in range(len(grilla[0])):
            if hay_jugador(grilla, c, f): 
                posicion = [f, c]
    return posicion

def mover_objetivo_con_caja(nueva_grilla, x_siguiente, y_siguiente, x_siguiente2, y_siguiente2):
    '''Recibe la nueva grilla armada, las coordenadas de la posición siguiente y las de la posición siguiente 2 (respecto a posición
    siguiente). Devuelve la grilla modificada simulando el movimiento de la caja que está sobre el objetivo'''
    nueva_grilla[x_siguiente][y_siguiente] = OBJETIVO_CON_JUGADOR
    if hay_espacio_vacio(nueva_grilla, y_siguiente2, x_siguiente2): 
        nueva_grilla[x_siguiente2][y_siguiente2] = CAJA
    elif nueva_grilla[x_siguiente2][y_siguiente2] == OBJETIVO: 
        nueva_grilla[x_siguiente2][y_siguiente2] = OBJETIVO_CON_CAJA
    return nueva_grilla

def mover_caja(nueva_grilla, x_siguiente, y_siguiente, posicion_siguiente2):
    '''Recibe la nueva grilla armada, las listas de posicion_siguiente (respecto al jugador) y posicion_siguiente2 (respecto a
    posicion_siguiente). Devuelve la grilla modificada simulando el movimiento de la caja'''
    [x_siguiente2, y_siguiente2] = posicion_siguiente2
    if nueva_grilla[x_siguiente][y_siguiente] == CAJA:
        nueva_grilla[x_siguiente][y_siguiente] = JUGADOR
        if hay_espacio_vacio(nueva_grilla, y_siguiente2, x_siguiente2): 
            nueva_grilla[x_siguiente2][y_siguiente2] = CAJA
        elif nueva_grilla[x_siguiente2][y_siguiente2] == OBJETIVO: 
            nueva_grilla[x_siguiente2][y_siguiente2] = OBJETIVO_CON_CAJA
    elif nueva_grilla[x_siguiente][y_siguiente] == OBJETIVO_CON_CAJA:
        mover_objetivo_con_caja(nueva_grilla, x_siguiente, y_siguiente, x_siguiente2, y_siguiente2)
    return nueva_grilla

def mover_jugador(nueva_grilla, x_jugador, y_jugador, posicion_siguiente, posicion_siguiente2):
    '''Recibe la nueva grilla armada, las coordenadas de la posición del jugador y las listas de posicion_siguiente (respecto al 
    jugador) y posicion_siguiente2 (respecto a posición_siguiente). Devuelve la grilla modificada simulando el movimiento del jugador'''
    [x_siguiente, y_siguiente] = posicion_siguiente
    if nueva_grilla[x_jugador][y_jugador] == JUGADOR: 
        nueva_grilla[x_jugador][y_jugador] = ESPACIO_VACIO
    elif nueva_grilla[x_jugador][y_jugador] == OBJETIVO_CON_JUGADOR: 
        nueva_grilla[x_jugador][y_jugador] = OBJETIVO
    if hay_espacio_vacio(nueva_grilla, y_siguiente, x_siguiente):
         nueva_grilla[x_siguiente][y_siguiente] = JUGADOR
    elif nueva_grilla[x_siguiente][y_siguiente] == OBJETIVO: 
        nueva_grilla[x_siguiente][y_siguiente] = OBJETIVO_CON_JUGADOR
    elif hay_caja(nueva_grilla, y_siguiente, x_siguiente): 
        mover_caja(nueva_grilla, x_siguiente, y_siguiente, posicion_siguiente2)
    return nueva_grilla

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    nueva_grilla = copiar_grilla(grilla)
    [x_jugador, y_jugador] = buscar_jugador(nueva_grilla)
    posicion_siguiente = [x_jugador + direccion[1], y_jugador + direccion[0]] 
    posicion_siguiente2 = [x_jugador + (2 * direccion[1]), y_jugador + (2 * direccion[0])]
    if not es_celda_vacia(grilla, posicion_siguiente, posicion_siguiente2): 
        return grilla
    nueva_grilla = mover_jugador(nueva_grilla, x_jugador, y_jugador, posicion_siguiente, posicion_siguiente2)
    return nueva_grilla

