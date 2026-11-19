-- Creacion del keyspace cercanias y de sus 4 tablas
-- Ejecutamos desde cqlsh:  SOURCE '/tmp/crear_tablas.cql';

CREATE KEYSPACE cercanias WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE cercanias;

-- Tabla 1: paradas de una linea en un dia, ordenadas por hora
CREATE TABLE paradas_por_linea_dia (
    linea text,
    sentido int,
    origen text,
    destino text,
    fecha_servicio date,
    tren text,
    estacion text,
    hora_prevista time,
    retraso_min int,
    hora_calculada time,
    PRIMARY KEY ((linea, fecha_servicio), hora_prevista, tren, estacion)
);

-- Tabla 2: recorrido de un tren en un dia, estacion por estacion
CREATE TABLE recorrido_por_tren_dia (
    linea text,
    sentido int,
    origen text,
    destino text,
    fecha_servicio date,
    tren text,
    estacion text,
    hora_prevista time,
    retraso_min int,
    hora_calculada time,
    PRIMARY KEY ((tren, fecha_servicio), hora_prevista, estacion)
);

-- Tabla 3: retrasos de una linea en un dia, de mayor a menor
CREATE TABLE retrasos_por_linea_dia (
    linea text,
    sentido int,
    origen text,
    destino text,
    fecha_servicio date,
    tren text,
    estacion text,
    hora_prevista time,
    retraso_min int,
    hora_calculada time,
    PRIMARY KEY ((linea, fecha_servicio), retraso_min, tren, estacion)
) WITH CLUSTERING ORDER BY (retraso_min DESC, tren ASC, estacion ASC);

-- Tabla 4: retrasos de una estacion a lo largo de los dias
CREATE TABLE retrasos_por_estacion (
    linea text,
    sentido int,
    origen text,
    destino text,
    fecha_servicio date,
    tren text,
    estacion text,
    hora_prevista time,
    retraso_min int,
    hora_calculada time,
    PRIMARY KEY ((estacion), fecha_servicio, hora_prevista, tren)
);

