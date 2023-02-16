def inicializar_niveles(ruta_entrada):
    '''Dado un archivo con los niveles disponibles en el juego carga todos en la memoria para que se puedan jugar.'''
    try:
        with open(ruta_entrada, 'r') as archivo:
            niveles = []
            nivel = []
            longitud_maxima = 0
            cant_niveles = 0
            for linea in archivo:
                linea = linea.rstrip('\n')
                if ('#' not in linea) and (linea != ''):
                    continue
                elif linea == '':
                    for i in range(len(nivel)):
                        nivel[i] += ((longitud_maxima - len(nivel[i])) * ' ') #ajusto la longitud de la línea
                    niveles.append(nivel)
                    cant_niveles += 1
                    nivel = []
                    longitud_maxima = 0
                    continue
                nivel.append(linea)
                if len(linea) > longitud_maxima: #busco la línea con mayor cantidad de elementos
                    longitud_maxima = len(linea)
            for i in range(len(nivel)): #agrego el último nivel
                nivel[i] += ((longitud_maxima - len(nivel[i])) * ' ')
                niveles.append(nivel)
            cant_niveles += 1
            return niveles, cant_niveles
    except FileNotFoundError:
        print(f'El archivo {ruta_entrada} no existe')
        raise
    except IndexError:
        print(f'El archivo {ruta_entrada} está corrupto o intentas acceder a una posición que no existe')
        raise