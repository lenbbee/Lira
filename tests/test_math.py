from src.radar_math import calcular_escala_zoom, coordenadas_polares_a_pixeles


def test_calcular_escala_zoom_positivo():
    zoom = calcular_escala_zoom(radio_radar_pixeles=250, distancia_max_visible_pc=500.0)
    assert zoom > 0


def test_coordenadas_devuelven_numeros():
    zoom = calcular_escala_zoom(radio_radar_pixeles=250, distancia_max_visible_pc=500.0)
    pixel_x, pixel_y = coordenadas_polares_a_pixeles(
        distancia_pc=300.0,
        angulo_grados=45.0,
        zoom_Z=zoom,
    )
    assert isinstance(pixel_x, (int, float))
    assert isinstance(pixel_y, (int, float))


def test_distancia_cero_queda_en_el_centro():
    radio = 250
    zoom = calcular_escala_zoom(radio_radar_pixeles=radio, distancia_max_visible_pc=500.0)
    pixel_x, pixel_y = coordenadas_polares_a_pixeles(
        distancia_pc=0.0,
        angulo_grados=0.0,
        zoom_Z=zoom,
    )
    # un planeta a distancia 0 debería caer en el origen del radar
    assert pixel_x == radio
    assert pixel_y == radio