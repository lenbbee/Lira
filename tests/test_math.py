from src.radar_math import calcular_escala_zoom, coordenadas_polares_a_pixeles
zoom = calcular_escala_zoom(radio_radar_pixeles=250, distancia_max_visible_pc=500.0)
pixel_x, pixel_y = coordenadas_polares_a_pixeles(
    distancia_pc= 300.0,
    angulo_grados= 45.0,
    zoom_Z = zoom
) 
print(f"Coordenadas en pantalla calculadas: X={pixel_x}, Y={pixel_y}")
