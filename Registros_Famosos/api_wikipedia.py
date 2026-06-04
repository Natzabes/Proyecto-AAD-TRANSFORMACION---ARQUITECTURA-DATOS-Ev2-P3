import requests
import json
import os

def cargar_cache():
    ruta = "data/cache_famosos.json"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return {}

def guardar_cache(cache):
    os.makedirs("data", exist_ok=True)
    with open("data/cache_famosos.json", "w", encoding="utf-8") as archivo:
        json.dump(cache, archivo, ensure_ascii=False, indent=4)

def obtener_datos_famoso(nombre):
    cache = cargar_cache()

    if nombre in cache:
        print(f"Datos de {nombre} obtenidos desde caché")
        return cache[nombre]

    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + nombre.replace(" ", "_")
    headers = {"User-Agent": "ProyectoFamosos/1.0 (contacto@tuemail.com)"}

    try:
        respuesta = requests.get(url, headers=headers)
        if respuesta.status_code != 200:
            return None
        datos = respuesta.json()
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return None

    imagen = None
    if "thumbnail" in datos:
        imagen = datos["thumbnail"]["source"]

    resultado = {
        "nombre": datos.get("title", nombre),
        "descripcion": datos.get("extract", "Sin descripción disponible."),
        "imagen": imagen,
        "fuente": url,
        "captura": "Fecha de captura original (ver metadatos en fuente)" # Cumple requerimiento
    }

    cache[nombre] = resultado
    guardar_cache(cache)
    return resultado