
USE cercanias;

-- CONSULTA 1: Disponibilidad de trenes en Chamartín
-- Líneas C-1, C-2 y C-3 entre las 13:00 y las 13:30

SELECT linea, tren, estacion, destino,
       hora_prevista, retraso_min, hora_calculada
FROM paradas_por_linea_dia
WHERE linea IN ('C-1', 'C-2', 'C-3')
AND fecha_servicio = '2026-10-21'
AND hora_prevista >= '13:00:00'
AND hora_prevista <= '13:30:00'
AND estacion = 'Madrid-Chamartín-Clara Campoamor'
ALLOW FILTERING;


-- CONSULTA 2: Horarios y retrasos de la línea C-5

SELECT tren, estacion, destino,
       hora_prevista, retraso_min, hora_calculada
FROM paradas_por_linea_dia
WHERE linea = 'C-5'
AND fecha_servicio = '2026-10-21'
LIMIT 15;


-- CONSULTA 3: Recorrido y evolución de retrasos de un tren

SELECT estacion, hora_prevista, retraso_min, hora_calculada
FROM recorrido_por_tren_dia
WHERE tren = '1092X19637C5'
AND fecha_servicio = '2026-10-21';


-- CONSULTA 4: Mayores retrasos de las cuatro líneas

-- Línea C-1
SELECT linea, tren, estacion, retraso_min
FROM retrasos_por_linea_dia
WHERE linea = 'C-1'
AND fecha_servicio = '2026-10-21'
LIMIT 10;

-- Línea C-2
SELECT linea, tren, estacion, retraso_min
FROM retrasos_por_linea_dia
WHERE linea = 'C-2'
AND fecha_servicio = '2026-10-21'
LIMIT 10;

-- Línea C-3
SELECT linea, tren, estacion, retraso_min
FROM retrasos_por_linea_dia
WHERE linea = 'C-3'
AND fecha_servicio = '2026-10-21'
LIMIT 10;

-- Línea C-5
SELECT linea, tren, estacion, retraso_min
FROM retrasos_por_linea_dia
WHERE linea = 'C-5'
AND fecha_servicio = '2026-10-21'
LIMIT 10;


-- CONSULTA 5: Retrasos registrados en Atocha Cercanías

SELECT linea, tren, fecha_servicio, destino,
       hora_prevista, retraso_min, hora_calculada
FROM retrasos_por_estacion
WHERE estacion = 'Madrid-Atocha Cercanías'
LIMIT 20;


-- CONSULTA 6: Evolución de los retrasos en Atocha
-- Del 19 al 23 de octubre de 2026

SELECT fecha_servicio, linea, tren, retraso_min,
       hora_prevista, hora_calculada
FROM retrasos_por_estacion
WHERE estacion = 'Madrid-Atocha Cercanías'
AND fecha_servicio >= '2026-10-19'
AND fecha_servicio <= '2026-10-23';
