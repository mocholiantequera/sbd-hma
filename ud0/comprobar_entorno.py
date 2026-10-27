"""Comprueba que el entorno de Python del módulo SBD está preparado."""
import importlib
import sys
from importlib.metadata import version as version_de
# (nombre con el que se importa, nombre del paquete en requirements.txt)
LIBRERIAS = [
 ("pandas", "pandas"),
 ("pyarrow", "pyarrow"),
 ("duckdb", "duckdb"),
 ("matplotlib", "matplotlib"),
 ("statsmodels", "statsmodels"),
 ("requests", "requests"),
 ("bs4", "beautifulsoup4"),
 ("dotenv", "python-dotenv"),
 ("boto3", "boto3"),
 ("awswrangler", "awswrangler"),
 ("psycopg2", "psycopg2-binary"),
 ("pdfplumber", "pdfplumber"),
 ("spacy", "spacy"),
]
problemas = 0
# 1. Versión de Python
v = sys.version_info
if v >= (3, 10):
 print(f"[OK] Python {v.major}.{v.minor}.{v.micro}")
else:
 print(f"[FALLO] Python {v.major}.{v.minor}: hace falta la 3.10 o superior")
 problemas += 1
# 2. Entorno virtual activo
if sys.prefix != sys.base_prefix:
 print(f"[OK] Entorno virtual activo en {sys.prefix}")
else:
 print("[FALLO] El entorno virtual NO está activo")
 problemas += 1
# 3. Librerías del módulo
for modulo, paquete in LIBRERIAS:
    try:
        importlib.import_module(modulo)
        print(f"[OK] {paquete} {version_de(paquete)}")
    except ImportError:
        print(f"[FALLO] Falta {paquete}")
        problemas += 1
print()
if problemas == 0:
 print("Todo listo: el entorno está preparado para el módulo.")
else:
 print(f"Hay {problemas} problema(s). Revisa el apartado de errores típicos del anexo.")