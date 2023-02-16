import soko

def inmutabilizar_nivel(estado):
    '''Devuelve una representación inmutable del estado recibido.'''
    resultado = ''
    for f in range(len(estado)):
        for c in range(len(estado[0])):
            resultado += estado[f][c]
        resultado += '\n'
    return resultado

def movimientos_posibles(estado):
    '''Devuelve una lista con los movimientos posibles en el estado actual del nivel recibido.'''
    resultado = []
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for movimiento in movimientos:
        if soko.mover(estado, movimiento) != estado:
            #busco aquellos movimientos que no me dejen en la misma situación, por ej si me muevo contra una pared
            resultado.append(movimiento)
    return resultado

def buscar_solucion(estado_inicial):
    '''Determina si existen soluciones para el estado inicial recibido y las devuelve en una serie de pasos.'''
    visitados = {}
    return backtrack(estado_inicial, visitados)

def backtrack(estado, visitados):
    '''Encuentra de manera recursiva la solución al estado recibido y la devuelve si pudo hacerlo.'''
    visitados[inmutabilizar_nivel(estado)] = estado
    if soko.juego_ganado(estado):
        #¡Encontramos la solución!
        return True, []
    for a in movimientos_posibles(estado):
        nuevo_estado = soko.mover(estado, a)
        if inmutabilizar_nivel(nuevo_estado) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solucion_encontrada:
            return True, [a] + acciones
    return False, None