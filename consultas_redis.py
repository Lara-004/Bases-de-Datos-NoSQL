import redis
import time

try:
    # Conexión con Redis Local
    operador = redis.Redis(host='localhost', port=6379, username='operador_via', password='pass_operador', decode_responses=True)
    panel = redis.Redis(host='localhost', port=6379, username='panel_estacion', password='pass_panel', decode_responses=True)

    # Verificación de la conexión (devuelve True / PONG si es correcta)
    if operador.ping() and panel.ping():
        print("Conexión establecida correctamente con Redis Local\n")

    # Inserción de tramos y tiempos de llegada
    tramos_c5 = [("Atocha-Embajadores", 3), ("Alcorcon-Mostoles", 4), ("Fuenlabrada-Humanes", 6), ("Embajadores-Laguna", 7)]
    for tramo, minutos in tramos_c5:
        operador.zadd("tramos:C-5", {tramo: minutos})
        print(f"Tramo insertado en C-5: {tramo} (Llegada: {minutos} min)")

    print()
    tramos_c1 = [("Recoletos-Atocha", 3), ("Chamartin-NuevosMinisterios", 4), ("FuenteMora-AeropuertoT4", 8)]
    for tramo, minutos in tramos_c1:
        operador.zadd("tramos:C-1", {tramo: minutos})
        print(f"Tramo insertado en C-1: {tramo} (Llegada: {minutos} min)")

    time.sleep(1)

    # Obtener elementos ordenados por tiempo de manera ascendente
    print("\nConsultando próximos trenes en línea C-5:")
    proximos_c5 = panel.zrange("tramos:C-5", 0, -1, withscores=True)
    for nombre, score in proximos_c5:
        print(f" Próximo tren: {nombre} (Tiempo estimado: {int(score)} min)")

    print("\nConsultando próximos trenes en línea C-1:")
    proximos_c1 = panel.zrange("tramos:C-1", 0, -1, withscores=True)
    for nombre, score in proximos_c1:
        print(f" Próximo tren: {nombre} (Tiempo estimado: {int(score)} min)")

    # Visualizar el tiempo (score) de un elemento a partir de su clave 
    score_tramo = panel.zscore("tramos:C-1", "Chamartin-NuevosMinisterios")
    print(f"\nTiempo obtenido mediante zscore para Chamartin-NuevosMinisterios: {int(score_tramo)} min")

    # Actualizar tiempo por retraso en la vía
    nuevo_score = operador.zincrby("tramos:C-1", 6, "Chamartin-NuevosMinisterios")
    print(f"Retraso aplicado en Chamartin-NuevosMinisterios. Nuevo tiempo: {int(nuevo_score)} min")
    print("Cola C-1 actualizada:", panel.zrange("tramos:C-1", 0, -1, withscores=True))

    # Borrar un elemento del conjunto cuando el tren ya ha llegado
    operador.zrem("tramos:C-1", "Recoletos-Atocha")
    print("\nTramo eliminado tras llegada del tren: Recoletos-Atocha")
    print("Tramos pendientes en C-1:", panel.zrange("tramos:C-1", 0, -1, withscores=True))

except redis.ConnectionError as e:
    print(f" Error de conexión a Redis: {e}")
except Exception as e:
    print(f" Error: {e}")