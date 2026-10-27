"""UD1 · Primera exploración de la muestra con pandas."""
import pandas as pd
pd.set_option("display.width", 120)
# icao24 se lee como texto: es un código, no un número
df = pd.read_csv("ud1/datos/avistamientos.csv", dtype={"icao24": "str"})
print("Filas y columnas:", df.shape)
print()
print("Tipos de cada columna:")
print(df.dtypes)
print()
print("Nulos por columna:")
print(df.isna().sum())
print()
print("Aeronaves distintas:", df["icao24"].nunique())
print()
print("Países con más avistamientos:")
print(df["origin_country"].value_counts().head(5))
# ¿A qué horas hay más tráfico?
# time_position es una marca Unix en UTC: se convierte y se pasa a hora local
df["momento"] = pd.to_datetime(df["time_position"], unit="s", utc=True)
df["hora_local"] = df["momento"].dt.tz_convert("Europe/Madrid").dt.hour
por_hora = df.groupby("hora_local").size()
print()
print("Avistamientos por hora local (las 5 más cargadas):")
print(por_hora.sort_values(ascending=False).head(5))