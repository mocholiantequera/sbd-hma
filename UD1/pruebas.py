import pandas as pd

# ------------------------------------------------------------------
# 1) Lectura de avistamientos y cálculo de día/hora local
# ------------------------------------------------------------------
df = pd.read_csv("ud1/datos/avistamientos.csv", dtype={"icao24": "str"})

local = pd.to_datetime(
    df["time_position"], unit="s", utc=True
).dt.tz_convert("Europe/Madrid")

df["dia"] = local.dt.day
df["hora_local"] = local.dt.hour

lunes = set(df.loc[df["dia"] == 21, "icao24"])
martes = set(df.loc[df["dia"] == 22, "icao24"])

print("Lunes:", len(lunes), "· Martes:", len(martes))
print("En total (unión): ", len(lunes | martes))
print("Los dos días (intersec.):", len(lunes & martes))
print("Solo el lunes: ", len(lunes - martes))
print("Solo el martes: ", len(martes - lunes))

# ------------------------------------------------------------------
# 2) Unión con el catálogo de aeronaves
# Unir dos tablas es aplicar esa relación. Pero si la cardinalidad no
# es la que se cree, el resultado cambia de tamaño sin avisar.
# ------------------------------------------------------------------
aeronaves = pd.read_csv("ud1/datos/aeronaves.csv", dtype={"icao24": "str"})

antes = len(df)
mal = df.merge(aeronaves, on="icao24", how="left")
print(f"Filas antes: {antes} · después de unir: {len(mal)}")

repetidas = aeronaves[aeronaves.duplicated("icao24", keep=False)]
print(repetidas)

aeronaves = aeronaves.drop_duplicates("icao24", keep="first")

enriquecido = df.merge(
    aeronaves, on="icao24", how="left", validate="many_to_one"
)

sin_catalogo = enriquecido["matricula"].isna()
print("Filas:", len(enriquecido))
print("Avistamientos sin datos de catálogo:", sin_catalogo.sum())
print(
    "Aeronaves que no están en el catálogo:",
    enriquecido.loc[sin_catalogo, "icao24"].nunique(),
)

# ------------------------------------------------------------------
# 3) Clasificación por fase de vuelo
# ------------------------------------------------------------------
# Normalizamos "on_ground" para que sea booleano de verdad
# (si viene como texto "True"/"False" también se convierte bien).
df["on_ground"] = (
    df["on_ground"]
    .replace({"True": True, "False": False, "true": True, "false": False})
    .astype("boolean")
)


def fase(en_tierra, altitud):
    """Asigna a cada avistamiento una y solo una fase de vuelo."""
    if pd.isna(en_tierra):
        return "desconocida"
    if en_tierra:
        return "en tierra"
    if pd.isna(altitud):
        return "desconocida"
    if altitud < 3000:
        return "despegue o aproximación"
    if altitud < 9000:
        return "ascenso o descenso"
    return "crucero"


df["fase"] = [
    fase(t, a) for t, a in zip(df["on_ground"], df["baro_altitude"])
]

print(df["fase"].value_counts())

import networkx as nx
g = nx.DiGraph()
g.add_weighted_edges_from([
 ("VLC", "MAD", 14), ("VLC", "BCN", 9), ("VLC", "PMI", 21), ("VLC",
"CDG", 6),
 ("MAD", "AGP", 11), ("BCN", "PMI", 17), ("PMI", "VLC", 20), ("MAD",
"VLC", 13),
])
print("Destinos directos desde VLC:", list(g.successors("VLC")))
print("Vuelos semanales que tocan VLC:", g.degree("VLC",
weight="weight"))
print("Cómo ir de PMI a AGP:", nx.shortest_path(g, "PMI", "AGP"))
print("Destinos por aeropuerto:", dict(g.out_degree()))

crucero_tarde = (
 (df["baro_altitude"] >= 9000) & (df["hora_local"] >= 18) &
(df["hora_local"] < 22)
)
print("Avistamientos en crucero entre las 18 y las 22 h:",
crucero_tarde.sum())

a = df["baro_altitude"] >= 9000
b = df["hora_local"] >= 18
print((~(a & b)).equals(~a | ~b))

altitud = df["baro_altitude"]
print("Por encima de 0 m: ", (altitud > 0).sum())
print("En 0 m o por debajo: ", (altitud <= 0).sum())
print("Entre las dos: ", (altitud > 0).sum() + (altitud <=
0).sum())
print("Filas del fichero: ", len(df))
print("Altitudes que faltan: ", altitud.isna().sum())
import time
codigos = list(range(1_000_000))
conjunto = set(codigos)
inicio = time.perf_counter()
for _ in range(200):
 999_999 in codigos
print(f"En la lista: {time.perf_counter() - inicio:.3f} s")
inicio = time.perf_counter()
for _ in range(200):
 999_999 in conjunto
print(f"En el conjunto: {time.perf_counter() - inicio:.6f} s")