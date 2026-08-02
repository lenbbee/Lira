from src.data_manager import obtener_exoplanetas, filtrar_habitables


def test_obtener_exoplanetas_devuelve_datos():
    planetas = obtener_exoplanetas()
    assert len(planetas) > 0


def test_primer_planeta_tiene_formato_valido():
    planetas = obtener_exoplanetas()
    primero = planetas[0]
    # el planeta debe traer al menos su nombre
    assert "pl_name" in primero


def test_filtrar_habitables_es_subconjunto():
    todos = obtener_exoplanetas()
    habitables = filtrar_habitables(todos)
    # nunca puede haber más habitables que el total
    assert len(habitables) <= len(todos)


def test_habitables_tienen_campos_esperados():
    todos = obtener_exoplanetas()
    habitables = filtrar_habitables(todos)
    if len(habitables) > 0:
        p = habitables[0]
        # verifica que existan las claves que usa tu programa
        assert "name" in p
        assert "dist" in p
        assert "temp" in p
        assert "dens" in p