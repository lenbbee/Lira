def clasificar_exoplanetas(planetas: list) -> list:
    """
    Toma la lista de exoplanetas habitables y les asigna una categoría (cluster) 
    junto con un color representativo para la interfaz.
    """
    planetas_clasificados = []

    for planeta in planetas:
        # Hacemos una copia para no alterar el diccionario original directamente
        p = planeta.copy()
        temp = p.get("temp", 250.0)
        dens = p.get("dens", 4.0)

        # Algoritmo de Clustering por condiciones físicas
        if 260.0 <= temp <= 295.0 and 3.8 <= dens <= 5.2:
            p["cluster"] = "Oasis Templado"
            p["color"] = "#00ff66"  # Verde Neón (Alta habitabilidad)
        elif temp < 260.0:
            p["cluster"] = "Mundo Glacial"
            p["color"] = "#00bfff"  # Azul Neón (Frío)
        else:
            p["cluster"] = "Invernadero Cálido"
            p["color"] = "#ff9900"  # Naranja Neón (Caliente)

        planetas_clasificados.append(p)

    return planetas_clasificados