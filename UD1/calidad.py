"""UD1 · Primer informe de calidad de la muestra."""
import pandas as pd
df = pd.read_csv("ud1/datos/avistamientos.csv", dtype={"icao24": "str"})
def linea(texto, valor):
 print(f" {texto:<38}{valor:>6}")
 print(f"Filas analizadas: {len(df)}")
print("\n1. COMPLETITUD · % de valores que faltan")
faltan = (df.isna().mean() * 100).round(1)
for columna, porcentaje in faltan[faltan > 0].items():
 linea(columna, f"{porcentaje} %")
print("\n2. UNICIDAD")
linea("Filas repetidas exactas", df.duplicated().sum())
linea("Misma aeronave en el mismo instante",
 df.duplicated(subset=["icao24", "time_position"]).sum())
print("\n3. VALIDEZ")
linea("Altitudes por encima de 15.000 m", (df["baro_altitude"] >
15000).sum())
fuera = ~df["latitude"].between(37.8, 40.9) | ~df["longitude"].between(-
1.6, 0.7)
linea("Posiciones fuera de la zona", fuera.sum())
print("\n4. COHERENCIA")
en_vuelo_sin_altitud = ~df["on_ground"] & df["baro_altitude"].isna()
linea("En vuelo pero sin altitud", en_vuelo_sin_altitud.sum())
print("\n5. FORMATO")
linea("Indicativos vacíos", df["callsign"].isna().sum())
linea("Indicativos que solo tienen espacios", (df["callsign"].str.strip()
== "").sum())
linea("Indicativos con espacios al final", df["callsign"].str.endswith("").sum())