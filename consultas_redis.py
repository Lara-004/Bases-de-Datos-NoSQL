import os
import redis
import time

# PARTE 1: REDIS LOCAL
# Conexión a Redis
operador = redis.Redis(host='localhost', port=6379, username='operador_via', password='pass_operador', decode_responses=True)
panel = redis.Redis(host='localhost', port=6379, username='panel_estacion', password='pass_panel', decode_responses=True)

tramos_c5 = [("Atocha-Embajadores", 3), ("Alcorcon-Mostoles", 4), ("Fuenlabrada-Humanes", 6), ("Embajadores-Laguna", 7)]
tramos_c1 = [("Recoletos-Atocha", 3), ("Chamartin-NuevosMinisterios", 4), ("FuenteMora-AeropuertoT4", 8)]

# Inserción de tramos
for tramo, minutos in tramos_c5:
    operador.zadd("tramos:C-5", {tramo: minutos})
    print(f"Tramo insertado en C-5: {tramo} ({minutos} min)")

print()
for tramo, minutos in tramos_c1:
    operador.zadd("tramos:C-1", {tramo: minutos})
    print(f"Tramo insertado en C-1: {tramo} ({minutos} min)")

# Próximos trenes ordenados por tiempo
print("\nPróximos trenes en C-5:")
for tramo, score in panel.zrange("tramos:C-5", 0, -1, withscores=True):
    print(f"-  {tramo}: {int(score)} min")

print("\nPróximos trenes en C-1:")
for tramo, score in panel.zrange("tramos:C-1", 0, -1, withscores=True):
    print(f"-  {tramo}: {int(score)} min")

# Consulta de un tramo concreto
tramo_buscado = "Chamartin-NuevosMinisterios"
score_tramo = panel.zscore("tramos:C-1", tramo_buscado)
if score_tramo is not None:
    print(f"\nTiempo para {tramo_buscado}: {int(score_tramo)} min")

# Actualización por retraso
nuevo_score = operador.zincrby("tramos:C-1", 6, "Chamartin-NuevosMinisterios")
print(f"\nRetraso en Chamartin-NuevosMinisterios. Nuevo tiempo: {int(nuevo_score)} min")
print("Cola C-1 actualizada:", panel.zrange("tramos:C-1", 0, -1, withscores=True))

# Borrado tras llegada del tren
operador.zrem("tramos:C-1", "Recoletos-Atocha")
print("\nTramo eliminado: Recoletos-Atocha")
print("Tramos pendientes en C-1:", panel.zrange("tramos:C-1", 0, -1, withscores=True))


# PARTE 2: REDIS CLOUD

cloud = redis.Redis(
    host='stew-integral-puff-51650.db.redis.io',
    port=14260,
    decode_responses=True,
    username="default",
    password="9yBlercRofvIy6WUTbRmTlBcmMMYVhrv",
)

success = cloud.set('foo', 'bar')

result = cloud.get('foo')
print(result)

# Estado de las estaciones
cloud.set("estado:Atocha", "abierta")
cloud.set("estado:Chamartin", "con demoras")
print("\nEstado de estaciones en Redis Cloud:")
print("- Atocha:", cloud.get("estado:Atocha"))
print("- Chamartin:", cloud.get("estado:Chamartin"))

# Top 3 desde el ZSET local a Redis Cloud con caducidad
top3_c5 = panel.zrange("tramos:C-5", 0, 2, withscores=True)
for tramo, minutos in top3_c5:
    cloud.zadd("top3:Atocha", {tramo: minutos})

cloud.expire("top3:Atocha", 10)  # Caduca en 10 segundos

print("\nTop 3 copiado a Cloud:", cloud.zrange("top3:Atocha", 0, -1, withscores=True))
print(f"TTL inicial: {cloud.ttl('top3:Atocha')} segundos")

time.sleep(4)
print(f"TTL tras 4 segundos: {cloud.ttl('top3:Atocha')} segundos")

time.sleep(7)
print('Top 3 tras superar los 10 segundos (caducado):', cloud.zrange('top3:Atocha', 0, -1, withscores=True))

print(f"TTL final de clave expirada: {cloud.ttl('top3:Atocha')}")