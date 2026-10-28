# F1. Conjuntos
# Calcular las aeronaves que aparecen solo por la mañana (antes de las 14 h), solo por la tarde y en las dos franjas

import duckdb
FICHERO = "ud1/datos/avistamientos.csv"
print("Aeronaves distintas por franja (solo mañana / solo tarde / ambas):")
duckdb.sql(f"""
    WITH local AS (
        SELECT icao24,
               hour(to_timestamp(time_position) AT TIME ZONE 'Europe/Madrid')
                   AS hora_local
        FROM '{FICHERO}'
    ),
    por_franja AS (
        SELECT DISTINCT
               icao24,
               CASE WHEN hora_local < 14 THEN 'manana' ELSE 'tarde' END AS franja
        FROM local
    ),
    agrupado AS (
        SELECT icao24,
               bool_or(franja = 'manana') AS manana,
               bool_or(franja = 'tarde')  AS tarde
        FROM por_franja
        GROUP BY icao24
    )
    SELECT
        count(*) FILTER (WHERE manana AND NOT tarde) AS solo_manana,
        count(*) FILTER (WHERE NOT manana AND tarde) AS solo_tarde,
        count(*) FILTER (WHERE manana AND tarde)     AS ambas,
        count(*)                                     AS total
    FROM agrupado
""").show()



#F2. Cardinalidad Identificar la cardinalidad entre avistamientos, aeronaves y operadores, y decir en qué tabla iría cada clave

print("----------------------------EJERCICIO 1 APARTADO F2----------------------------------")
import pandas as pd
avistamientos = pd.read_csv("ud1/datos/avistamientos.csv")
aeronaves = pd.read_csv("ud1/datos/aeronaves.csv")

# 1. Validar Avistamientos N:1 Aeronaves (Lo que ya tienes)
aeronaves = aeronaves.drop_duplicates("icao24", keep="first")

avistamientos_enriquecidos = avistamientos.merge(
    aeronaves,
    on="icao24",
    how="left",
    validate="many_to_one"
)

sin_catalogo = avistamientos_enriquecidos["matricula"].isna()

print("--- VALIDACIÓN AVISTAMIENTOS -> AERONAVES ---")
print("Filas totales:", len(avistamientos_enriquecidos))
print("Avistamientos sin datos de catálogo:", sin_catalogo.sum())
print("Aeronaves distintas no catalogadas:", avistamientos_enriquecidos.loc[sin_catalogo, "icao24"].nunique())

# 2. Validar Aeronaves N:1 Operadores (Opcional, para completar)
# Creamos un catálogo de operadores para probar la relación
operadores = aeronaves[['operador']].drop_duplicates().dropna()

aeronaves_con_operador = aeronaves.merge(
    operadores,
    on="operador",
    how="left",
    validate="many_to_one"
)



print("\n--- VALIDACIÓN AERONAVES -> OPERADORES ---")
print("Total de aeronaves en catálogo:", len(aeronaves_con_operador))
print("Aeronaves sin operador asignado:", aeronaves_con_operador['operador'].isna().sum())




#F3. Función total Escribir una función que clasifique la velocidad en tres categorías y demostrar con los datos que no deja ninguna fila sin clasificar
import pandas as pd
df = pd.read_csv("ud1/datos/avistamientos.csv", dtype={"velocity": "float64"})
def clasificar_velocidad(valor):
    valor = float(valor)
    if valor < 100:
        return "Velocidad baja"
    elif valor < 200:
        return "Velocidad media"
    elif valor is None:
        return "Sin datos"
    else:
        return "Velocidad alta"
    


print("----------------------------EJERCICIO 1 APARTADO F3----------------------------------")

df["clase_velocidad"] = [clasificar_velocidad(v) for v in df["velocity"]]
print(df["clase_velocidad"].value_counts())


# F4. Clave e inyectividad Comprobar si icao24 junto con time_position identifica cada fila, y encontrar las filas que lo impiden

print("----------------------------EJERCICIO 1 APARTADO F4----------------------------------")
import pandas as pd

# (Asumimos que 'avistamientos' ya está cargado en memoria)
# avistamientos = pd.read_csv("tu_archivo_avistamientos.csv")

# 1. Definimos la clave candidata
clave = ["icao24", "time_position"]

# 2. Buscamos las filas duplicadas según esa clave
# keep=False marca como True TODAS las filas que pertenecen a un grupo de duplicados
filas_duplicadas = avistamientos[avistamientos.duplicated(subset=clave, keep=False)]

# 3. Las ordenamos por la clave para que sea fácil verlas juntas
filas_duplicadas = filas_duplicadas.sort_values(by=clave)

# 4. Mostrar resultados
print("--- ANÁLISIS DE CLAVE (icao24 + time_position) ---")
print(f"Total de filas implicadas en duplicados: {len(filas_duplicadas)}")
print(f"Pares (icao24, time_position) que se repiten: {filas_duplicadas.groupby(clave).ngroups}\n")

if len(filas_duplicadas) > 0:
    print("❌ La combinación NO identifica cada fila de forma única.")
    print("Estas son las filas que lo impiden:\n")
    # Mostramos solo algunas columnas para que la consola no se sature
    print(filas_duplicadas[["icao24", "time_position", "callsign", "origin_country"]])
else:
    print("✅ La combinación SÍ identifica cada fila de forma única (es inyectiva).")

# 5. (Opcional) Cuántas filas tendríamos que borrar para arreglarlo
copias_sobrantes = avistamientos.duplicated(subset=clave).sum()
print(f"\nSi elimináramos las copias sobrantes con drop_duplicates, borraríamos {copias_sobrantes} filas.")

# 6. (Opcional) Crear la versión limpia que sí cumple la inyectividad
avistamientos_limpios = avistamientos.drop_duplicates(subset=clave).copy()
print(f"Filas restantes tras limpiar: {len(avistamientos_limpios)}")


#F5. Grafos Añadir dos rutas al grafo del apartado 6.4 y calcular de nuevo el grado de VLC y un camino que antes no existía

print("----------------------------EJERCICIO 1 APARTADO F5----------------------------------")
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


# F7. Nulos Mostrar con un ejemplo de la muestra que una comparación con un valor que falta da falso, y arreglarlo

print("----------------------------EJERCICIO 1 APARTADO F7----------------------------------")

import pandas as pd

# 1. Extraemos una muestra de ejemplo (3 filas que sabemos que tienen nulos)
muestra = avistamientos[avistamientos["baro_altitude"].isna()].head(3).copy()

print("--- 1. LA MUESTRA (Filas con altitud nula) ---")
print(muestra[["icao24", "time_position", "baro_altitude"]])


print("\n--- 2. EL PROBLEMA: Comparar con un nulo da Falso ---")
print("¿Es mayor que 0?")
print(muestra["baro_altitude"] > 0)

print("\n¿Es menor o igual que 0?")
print(muestra["baro_altitude"] <= 0)

print("\nAl sumar ambas condiciones, las filas con nulos no cuentan en ninguna:")
suma_muestra = (muestra["baro_altitude"] > 0).sum() + (muestra["baro_altitude"] <= 0).sum()
print(f"Suma de condiciones: {suma_muestra}")
print(f"Total de filas de la muestra: {len(muestra)}")
print(f"¡Faltan {len(muestra) - suma_muestra} filas! (Porque ambas comparaciones dieron False)")


print("\n--- 3. EL ARREGLO ---")
# Opción A: Rellenar los nulos antes de comparar (por ejemplo, con 0)
muestra_arreglada = muestra["baro_altitude"].fillna(0)
print("Opción A: Usando fillna(0) antes de comparar")
print(f"Suma de condiciones: {(muestra_arreglada > 0).sum() + (muestra_arreglada <= 0).sum()}")
print(f"Total de filas: {len(muestra)} (¡Ahora sí cuadra!)")

# Opción B: Contar los nulos explícitamente en la suma
print("\nOpción B: Añadiendo los nulos explícitamente a la suma")
suma_con_nulos = (muestra["baro_altitude"] > 0).sum() + (muestra["baro_altitude"] <= 0).sum() + muestra["baro_altitude"].isna().sum()
print(f"Suma de condiciones + nulos: {suma_con_nulos}")
print(f"Total de filas: {len(muestra)} (¡También cuadra!)")




# F8. Complejidad Cronometrar la búsqueda de 1000 códigos icao24 en una lista y en un conjunto, y explicar la diferencia

import time

print("----------------------------EJERCICIO 1 APARTADO F8----------------------------------")

# 1. Preparamos los datos
# Extraemos los icao24 reales que hay en el dataframe (sin nulos)
codigos_icao = avistamientos['icao24'].dropna().unique().tolist()

# Nos aseguramos de tener 1000 códigos para buscar (si hay menos, los repetimos)
codigos_a_buscar = (codigos_icao * (1000 // len(codigos_icao) + 1))[:1000]

# 2. Creamos las dos estructuras
lista_icao = list(codigos_icao)
conjunto_icao = set(codigos_icao)

# 3. Cronometramos la búsqueda en la LISTA (O(n))
inicio = time.perf_counter()
for codigo in codigos_a_buscar:
    _ = codigo in lista_icao
tiempo_lista = time.perf_counter() - inicio

# 4. Cronometramos la búsqueda en el CONJUNTO (O(1))
inicio = time.perf_counter()
for codigo in codigos_a_buscar:
    _ = codigo in conjunto_icao
tiempo_conjunto = time.perf_counter() - inicio

# 5. Mostramos los resultados
print(f"Buscando {len(codigos_a_buscar)} códigos en total...")
print(f"En la lista:    {tiempo_lista:.6f} s")
print(f"En el conjunto: {tiempo_conjunto:.8f} s")