from vectores import *
def area_triangulo(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    '''Recibe las coordenadas de tres puntos en R3 y devuelve el área del triángulo que conforman'''
    (ab1, ab2, ab3) = diferencia(x1, y1, z1, x2, y2, z2)
    (ac1, ac2, ac3) = diferencia(x1, y1, z1, x3, y3, z3)
    (v1, v2, v3) = calculo_producto_vectorial(ab1, ab2, ab3, ac1, ac2, ac3)
    norma_vector = norma(v1, v2, v3)
    area = norma_vector / 2
    return area

assert (area_triangulo(5, 8 , -1, -2, 3, 4, -3, 3, 0))
assert (area_triangulo(2, 5, 8, -3, -4, -3, 2, 1, 1))
assert (area_triangulo(6, 6, 9, 5, 4, 3, 7, -2, -2))




