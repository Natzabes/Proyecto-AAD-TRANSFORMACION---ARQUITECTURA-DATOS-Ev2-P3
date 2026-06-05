import requests
import json
import os
from datetime import datetime


def cargar_cache():

    ruta = (
        "data/cache_famosos.json"
    )

    if os.path.exists(ruta):

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(
                archivo
            )

    return {}

def guardar_cache(cache):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        "data/cache_famosos.json",
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            cache,
            archivo,
            ensure_ascii=False,
            indent=4
        )

def obtener_datos_famoso(nombre):

    cache = cargar_cache()

    if nombre in cache:

        print(
            "Datos obtenidos desde caché"
        )

        return cache[nombre]

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + nombre.replace(" ", "_")
    )

    headers = {
        "User-Agent":
        "ProyectoFamosos/1.0"
    }

    respuesta = requests.get(
        url,
        headers=headers
    )

    datos = respuesta.json()

    imagen = None

    if "thumbnail" in datos:

        imagen = datos[
            "thumbnail"
        ]["source"]

    resultado = {
        "nombre": datos.get(
            "title"
        ),
        "descripcion": datos.get(
            "extract"
        ),
        "fecha_consulta":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "imagen": imagen,
        "fuente": url
    }

    cache[nombre] = resultado

    guardar_cache(
        cache
    )

    return resultado

if __name__ == "__main__":

    nombre = input(
        "Ingrese famoso: "
    )

    datos = obtener_datos_famoso(
        nombre
    )

    print(datos)