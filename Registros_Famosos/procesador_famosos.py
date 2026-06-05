import pandas as pd
from datetime import datetime
import os

def calcular_edad(fecha_nacimiento):

    try:

        fecha = datetime.strptime(
            fecha_nacimiento,
            "%d-%m-%Y"
        )

        hoy = datetime.now()

        edad = (
            hoy.year
            - fecha.year
        )

        if (
            hoy.month,
            hoy.day
        ) < (
            fecha.month,
            fecha.day
        ):
            edad -= 1

        return edad

    except:

        return "N/A"

def procesar_famosos(
    ruta_archivo
):
    df = pd.read_csv(
    ruta_archivo
)
    antes = len(df)

    df = df.drop_duplicates()

    despues = len(df)

    duplicados_eliminados = (
        antes - despues
    )

    df["EDAD"] = (
    df["FECHA_NACIMIENTO"]
    .apply(calcular_edad)
)
    os.makedirs(
    "outputs",
    exist_ok=True
)
    df.to_csv(
    "outputs/famosos_consolidados.csv",
    index=False,
    encoding="utf-8-sig"
)
    
    print(
        f"Registros leídos: {antes}"
    )

    print(
        f"Duplicados eliminados: {duplicados_eliminados}"
    )

    print(
        f"Famosos procesados: {len(df)}"
    )
    
    print(
    "\nArchivo generado correctamente."
)