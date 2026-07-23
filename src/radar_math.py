import math

def grados_a_radianes(grados: float) -> float:
    radianes = grados * (math.pi / 180)
    return radianes


def calcular_escala_zoom(radio_radar_pixeles: int, distancia_max_visible_pc: float) -> float:
    z = radio_radar_pixeles / distancia_max_visible_pc
    return z


def coordenadas_polares_a_pixeles(
    distancia_pc: float, 
    angulo_grados: float, 
    zoom_Z: float, 
    centro_x: int = 250, 
    centro_y: int = 250
) -> tuple[int, int]:
    # 1. Convierte el ángulo de grados a radianes usando tu función anterior.
    radianes = grados_a_radianes(angulo_grados)
    # 2. Calcula X_real e Y_real usando math.cos() y math.sin().}
    x_real = distancia_pc * math.cos(radianes)
    y_real = distancia_pc * math.sin(radianes)
    x_pixel = centro_x + (x_real * zoom_Z)
    y_pixel = centro_y - (y_real * zoom_Z)
    # 4. Retorna una tupla con los píxeles enteros (X_pixel, Y_pixel).
    return (int(x_pixel), int(y_pixel))