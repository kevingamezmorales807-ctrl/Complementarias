import pandas as pd
import numpy as np

# 1. Cargar archivo de calificaciones crudas
df = pd.read_csv("calificaciones_crudas.csv")

print("=== PRIMERAS FILAS (CRUDAS) ===")
print(df.head())
print("\nTamaño:", df.shape)

# 2. Normalizar nombres de columnas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# 3. Detectar columna de calificaciones
col_calif = None
for col in df.columns:
    if "calif" in col:
        col_calif = col
        break

if col_calif is None:
    raise ValueError("No encontré una columna que contenga la palabra 'calif'.")

print(f"\nColumna de calificación detectada: {col_calif}")

# 4. Quitar duplicados
antes = df.shape[0]
df = df.drop_duplicates()
despues = df.shape[0]
print(f"\nDuplicados eliminados: {antes - despues}")

# 5. Limpiar texto
cols_texto = df.select_dtypes(include=["object"]).columns
for col in cols_texto:
    df[col] = df[col].astype(str).str.strip()

# 6. Convertir calificaciones a número
df[col_calif] = pd.to_numeric(df[col_calif], errors="coerce")

print("\n=== ESTADÍSTICAS DE CALIFICACIONES ===")
print(df[col_calif].describe())

# 7. Manejo de valores faltantes
df[col_calif] = df[col_calif].fillna(df[col_calif].mean())

# 8. Asegurar rango válido 0–100
df[col_calif] = df[col_calif].clip(lower=0, upper=100)

# 9. Columna aprobados/reprobados
df["estado"] = np.where(df[col_calif] >= 70, "Aprobado", "Reprobado")

print("\n=== APROBADOS / REPROBADOS ===")
print(df["estado"].value_counts())

# 10. Guardar archivo limpio
df. to_csv("calificaciones_limpias.csv", index=False, encoding="utf-8-sig") 

print("\nLimpieza terminada. Archivo guardado como 'calificaciones_limpias.csv'.")