import backtracking

def deshacer_movimiento(juego):
    '''Deshace el último movimiento hecho, siempre que el nivel no esté en el estado inicial.'''
    if not juego['deshacer'].esta_vacia():
        juego['rehacer'].apilar(juego['grilla'])
        juego['grilla'] = juego['deshacer'].desapilar()
    while not juego['pistas'].esta_vacia():
        juego['pistas'].desencolar()

def rehacer_movimiento(juego):
    '''Rehace el último movimiento deshecho, siempre que se haya deshecho alguno antes.'''
    if not juego['rehacer'].esta_vacia():
        juego['deshacer'].apilar(juego['grilla'])
        juego['grilla'] = juego['rehacer'].desapilar()
    while not juego['pistas'].esta_vacia():
        juego['pistas'].desencolar()

def buscar_pistas(juego):
    '''Busca pistas para la solución de un determinado estado, si lo consigue las carga en el juego.'''
    encontrado, pasos = backtracking.buscar_solucion(juego['grilla'])
    if encontrado:
        for paso in pasos:
            juego['pistas'].encolar(paso)

def resetear_estados(juego):
    '''Reinicia las funciones del juego a su valor por defecto.'''
    while not juego['deshacer'].esta_vacia():
        juego['deshacer'].desapilar()
    while not juego['rehacer'].esta_vacia():
        juego['rehacer'].desapilar()
    while not juego['pistas'].esta_vacia():
        juego['pistas'].desencolar()