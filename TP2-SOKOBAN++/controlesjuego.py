MOVER_NORTE = (0, -1)
MOVER_SUR = (0, 1)
MOVER_OESTE = (-1, 0)
MOVER_ESTE = (1, 0)

def definir_controles(ruta_entrada):
    '''Dado un archivo con movimientos posibles, devuelve un diccionario con los controles para jugar donde cada clave es la tecla
    a presionar y el valor la acción asociada.'''
    teclas = {}
    acciones = {'NORTE': MOVER_NORTE, 'SUR': MOVER_SUR, 'ESTE': MOVER_ESTE, 'OESTE': MOVER_OESTE}
    try:
        with open(ruta_entrada, 'r') as archivo:
            for linea in archivo:
                linea = linea.rstrip('\n')
                if linea == '':
                    continue
                tecla, accion = linea.split(' = ') 
                if accion in acciones:
                    teclas[tecla] = acciones[accion]
                else:
                    teclas[tecla] = accion
        return teclas
    except FileNotFoundError:
        print(f'El archivo {ruta_entrada} no existe')
        raise
    except IndexError:
        print(f'El archivo {ruta_entrada} está corrupto o intentas acceder a una posición que no existe')
        raise