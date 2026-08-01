from src.data_manager import obtener_exoplanetas

print("🛰️ Conectando con el archivo de la NASA (esto puede tardar unos segundos)...")

# Llamamos a tu función pro. La primera vez debería ir a internet.
planetas = obtener_exoplanetas()

print("\n--- RESULTADOS DE LA AUDITORÍA DE DATOS ---")
print(f"📊 Cantidad total de exoplanetas detectados: {len(planetas)}")

if len(planetas) > 0:
    #Mostramos los datos crudos del primer planeta de la lista para verificar el formato
    print("🪐 Muestra del primer exoplaneta en la base de datos:")
    print(planetas[0])
    print("\n✅ ¡La prueba fue un éxito rotundo!")
else:
    print("❌ No se recibieron datos. Revisa tu conexión a internet o la URL.")

from src.data_manager import obtener_exoplanetas, filtrar_habitables

print("🚀 Cargando base de datos...")
todos_los_planetas = obtener_exoplanetas()

print("🔬 Aplicando filtros científicos de habitabilidad...")
habitables = filtrar_habitables(todos_los_planetas)

print(f"\n📊 ¡Filtro completado!")
print(f"🌍 Encontrados {len(habitables)} exoplanetas rocosos potencialmente habitables a menos de 200 pc.")

if len(habitables) > 0:
    print("\n🪐 Muestra de los candidatos encontrados:")
    for p in habitables[:3]:  # Mostramos los primeros 3 para revisar
        print(f"- {p['name']}: Distancia={p['dist']}pc, Temp={p['temp']}K, Dens={p['dens']}g/cm3")