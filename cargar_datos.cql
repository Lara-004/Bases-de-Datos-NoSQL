-- Carga de cercanias.csv en las 4 tablas del keyspace cercanias
-- Ejecutar desde cqlsh:  SOURCE '/tmp/cargar_datos.cql';


USE cercanias;
CONSISTENCY ONE;

COPY paradas_por_linea_dia (linea, sentido, origen, destino, fecha_servicio, tren, estacion, hora_prevista, retraso_min, hora_calculada)
FROM '/tmp/cercanias.csv' WITH HEADER = TRUE;

COPY recorrido_por_tren_dia (linea, sentido, origen, destino, fecha_servicio, tren, estacion, hora_prevista, retraso_min, hora_calculada)
FROM '/tmp/cercanias.csv' WITH HEADER = TRUE;

COPY retrasos_por_linea_dia (linea, sentido, origen, destino, fecha_servicio, tren, estacion, hora_prevista, retraso_min, hora_calculada)
FROM '/tmp/cercanias.csv' WITH HEADER = TRUE;

COPY retrasos_por_estacion (linea, sentido, origen, destino, fecha_servicio, tren, estacion, hora_prevista, retraso_min, hora_calculada)
FROM '/tmp/cercanias.csv' WITH HEADER = TRUE;
