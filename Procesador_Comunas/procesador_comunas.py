import pandas as pd
import os
from datetime import datetime
from unidecode import unidecode
from difflib import get_close_matches

def normalizar_texto(texto, formato):

    texto = str(texto).strip()

    if formato == "mayusculas":

        return texto.upper()

    elif formato == "minusculas":

        return texto.lower()

    elif formato == "titulo":

        return texto.title()

    return texto

def limpiar_comparacion(texto):

    texto = str(texto)

    texto = unidecode(texto)

    return texto.lower().strip()

def buscar_sugerencias(
    comuna,
    lista_comunas
):

    return get_close_matches(
        comuna,
        lista_comunas,
        n=5,
        cutoff=0.5
    )

def procesar_archivo_comunas(
    ruta_archivo,
    formato="titulo"
    
):
    try:

        print("Procesando archivo...")

        extension = os.path.splitext(
            ruta_archivo
        )[1].lower()

        if extension == ".csv":

            df = pd.read_csv(
                ruta_archivo,
                encoding="utf-8"
            )

        elif extension == ".txt":

            df = pd.read_csv(
                ruta_archivo,
                names=["COMUNA"],
                encoding="utf-8"
            )

        else:

            raise Exception(
                "Formato no soportado"
            )

        print(df.head())

        registros_leidos = len(df)

        antes = len(df)

        df = df.drop_duplicates()

        despues = len(df)

        duplicados_eliminados = (
            antes - despues
        )

        df["COMUNA"] = (
            df["COMUNA"]
            .apply(
                lambda x:
                normalizar_texto(x, formato)
            )
        )

        df_oficial = pd.read_csv(
            "data/Poblacion-Comunas-de-Chie-INE-2015-2020.csv"
        )

        df_oficial["COMPARACION"] = (
            df_oficial["COMUNA"]
            .apply(limpiar_comparacion)
        )

        lista_comunas = (
            df_oficial["COMPARACION"]
            .tolist()
        )

        df_oficial["COMUNA_NORMALIZADA"] = (
            df_oficial["COMUNA"]
            .apply(
                lambda x:
                normalizar_texto(x, formato)
            )
        )

        print(
            f"Comunas oficiales: {len(df_oficial)}"
        )

        print(
            f"Registros leídos: {registros_leidos}"
        )

        print(
            f"Duplicados eliminados: {duplicados_eliminados}"
        )
        
        consolidados = []
        procesadas = 0
        consolidadas = 0
        no_encontradas = 0
        errores = 0

        for _, fila in df.iterrows():

            comuna = fila["COMUNA"]

            comuna_comparacion = (
                limpiar_comparacion(comuna)
            )

            resultado = df_oficial[
                df_oficial["COMPARACION"]
                == comuna_comparacion
            ]

            if not resultado.empty:

                region = resultado.iloc[0]["REGION"]

                habitantes = resultado.iloc[0]["HABITANTES"]

                consolidados.append({
                    "COMUNA": resultado.iloc[0]["COMUNA"],
                    "REGION": region,
                    "HABITANTES": habitantes
                })

                consolidadas += 1

            else:

                no_encontradas += 1

                sugerencias = buscar_sugerencias(
                    comuna_comparacion,
                    lista_comunas
                )

                print(
                    f"\nComuna no encontrada: {comuna}"
                )

                if sugerencias:

                    print(
                        "Sugerencias:"
                    )

                    for sugerencia in sugerencias:

                        nombre_real = df_oficial[
                            df_oficial["COMPARACION"]
                            == sugerencia
                        ].iloc[0]["COMUNA"]

                        print(
                            f"- {nombre_real}"
                        )

            procesadas += 1

        df_final = pd.DataFrame(
            consolidados
        )

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        df_final.to_csv(
            "outputs/comunas_consolidadas.csv",
            index=False,
            encoding="utf-8-sig"
        )

        print("\nResumen")

        print(
            f"Procesadas: {procesadas}"
        )

        print(
            f"Consolidadas: {consolidadas}"
        )

        print(
            f"No encontradas: {no_encontradas}"
        )

        fecha_ejecucion = (
            datetime.now()
            .strftime("%Y-%m-%d %H:%M:%S")
        )

        os.makedirs(
            "logs",
            exist_ok=True
        )

        with open(
            "logs/auditoria.txt",
            "a",
            encoding="utf-8"
        ) as log:

            log.write(
                "\n" + "=" * 50 + "\n"
            )

            log.write(
                f"Fecha ejecución: {fecha_ejecucion}\n"
            )

            log.write(
                f"Registros leídos: {registros_leidos}\n"
            )

            log.write(
                f"Comunas procesadas: {procesadas}\n"
            )

            log.write(
                f"Duplicados eliminados: {duplicados_eliminados}\n"
            )

            log.write(
                f"Consolidadas: {consolidadas}\n"
            )

            log.write(
                f"No encontradas: {no_encontradas}\n"
            )

            log.write(
                f"Errores: {errores}\n"
            )

    except Exception as e:

        errores += 1

        print(
            f"Error: {e}"
        )

        os.makedirs(
            "logs",
            exist_ok=True
        )

        with open(
            "logs/errores.txt",
            "a",
            encoding="utf-8"
        ) as log_error:

            log_error.write(
                f"{datetime.now()} - {e}\n"
            )