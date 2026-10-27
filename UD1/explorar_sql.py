"""UD1 · La misma exploración, en SQL y con DuckDB."""
import duckdb
FICHERO = "ud1/datos/avistamientos.csv"
print("¿Cuántas filas y cuántas aeronaves distintas?")
duckdb.sql(f"""
 SELECT count(*) AS filas,
 count(DISTINCT icao24) AS aeronaves
 FROM '{FICHERO}'
""").show()
print("Países con más avistamientos:")
duckdb.sql(f"""
 SELECT origin_country AS pais, count(*) AS avistamientos
 FROM '{FICHERO}'
 GROUP BY pais
 ORDER BY avistamientos DESC
 LIMIT 5
""").show()
print("Las cinco horas locales con más tráfico:")
duckdb.sql(f"""
 SELECT hour(to_timestamp(time_position) AT TIME ZONE 'Europe/Madrid')
AS hora_local,
 count(*) AS avistamientos
 FROM '{FICHERO}'
 GROUP BY hora_local
 ORDER BY avistamientos DESC
 LIMIT 5
""").show()