import redis

try:
    # 1. Conexiones locales autenticadas con cada usuario ACL
    operador = redis.Redis(
        host='localhost',
        port=6379,
        username='operador_via',
        password='pass_operador',
        decode_responses=True
    )

    panel = redis.Redis(
        host='localhost',
        port=6379,
        username='panel_estacion',
        password='pass_panel',
        decode_responses=True
    )

    if operador.ping() and panel.ping():
        print("Conexión a Redis Local exitosa con usuarios ACL.")

    # 2. Carga de tramos y tiempos estimados de llegada con operador_via
    print("1. CARGA INICIAL DE TRAMOS")
    operador.zadd("tramos:C-5", {
        "Atocha-Embajadores": 3,
        "Alcorcon-Mostoles": 4,
        "Fuenlabrada-Humanes": 6,
        "Embajadores-Laguna": 7
    })
    operador.zadd("tramos:C-1", {
        "Recoletos-Atocha": 3,
        "Chamartin-NuevosMinisterios": 4,
        "FuenteMora-AeropuertoT4": 8
    })
    print("Tramos de las líneas C-5 y C-1 registrados correctamente.")

    # 3. Consulta de próximos trenes en llegar ordenados por tiempo con panel_estacion
    print("\n2. PRÓXIMOS TRENES EN LÍNEA C-5")
    lista_c5 = panel.zrange("tramos:C-5", 0, -1, withscores=True)
    for tramo, minutos in lista_c5:
        print(f"Tramo: {tramo} -> Llegada en {int(minutos)} min")

    print("\nRANKING INICIAL LÍNEA C-1")
    lista_c1 = panel.zrange("tramos:C-1", 0, -1, withscores=True)
    for tramo, minutos in lista_c1:
        print(f"Tramo: {tramo} -> Llegada en {int(minutos)} min")

    # 4. Consulta del tiempo de un tramo concreto con panel_estacion
    print("\n3. CONSULTA DE UN TRAMO CONCRETO")
    minutos = panel.zscore("tramos:C-1", "Chamartin-NuevosMinisterios")
    print(f"Tiempo estimado en Chamartin-NuevosMinisterios: {int(minutos)} min")

    # 5. Simulación de un retraso sumando minutos con operador_via
    print("\n4. SIMULACIÓN DE RETRASO (+6 MIN)")
    minutos_con_retraso = operador.zincrby("tramos:C-1", 6, "Chamartin-NuevosMinisterios")
    print(f"Nuevo tiempo en Chamartin-NuevosMinisterios tras incidencia: {int(minutos_con_retraso)} min")
    print("Ranking actualizado de C-1:", panel.zrange("tramos:C-1", 0, -1, withscores=True))

    # 6. Eliminación de un tren que ya ha completado su tramo con operador_via
    print("\n5. LIMPIEZA DE TRAMO COMPLETADO")
    operador.zrem("tramos:C-1", "Recoletos-Atocha")
    print("Tren en Recoletos-Atocha finalizado y eliminado.")
    print("Tramos activos restantes en C-1:", panel.zrange("tramos:C-1", 0, -1, withscores=True))

except redis.ConnectionError as error:
    print(f"Error de conexión a Redis: {error}")
except Exception as error:
    print(f"Error durante la ejecución: {error}")