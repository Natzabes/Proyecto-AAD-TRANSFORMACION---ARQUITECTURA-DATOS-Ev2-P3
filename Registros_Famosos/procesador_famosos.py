import pandas as pd
from datetime import datetime
import os

def calcular_edad(fecha_nacimiento):
    try:
        # Intentar formato estándar
        fecha = datetime.strptime(str(fecha_nacimiento), "%Y-%m-%d")
        hoy = datetime.now()
        edad = hoy.year - fecha.year
        if (hoy.month, hoy.day) < (fecha.month, fecha.day):
            edad -= 1
        return edad
    except ValueError:
        # Manejo básico si viene solo el año o un formato extraño (ej. Julius Caesar)
        try:
            año = int(str(fecha_nacimiento).split("-")[0])
            return datetime.now().year - año
        except:
            return "N/A"

def procesar_famosos(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return

    df = pd.read_csv(ruta_archivo)
    antes = len(df)
    df = df.drop_duplicates()
    despues = len(df)

    # Corregido: Se aplica solo una vez
    df["EDAD"] = df["FECHA_NACIMIENTO"].apply(calcular_edad)

    os.makedirs("outputs", exist_ok=True)
    df.to_csv("outputs/famosos_consolidados.csv", index=False, encoding="utf-8-sig")
    
    print(f"Registros leídos: {antes}")
    print(f"Duplicados eliminados: {antes - despues}")
    print(f"Famosos procesados con éxito.")