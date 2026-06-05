import tkinter as tk

from PIL import (
    Image,
    ImageTk
)

import requests
from io import BytesIO

def mostrar_famoso(datos):
    ventana = tk.Toplevel()

    ventana.title(
        datos["nombre"]
    )

    ventana.geometry(
        "600x700"
    )

    lbl_nombre = tk.Label(
        ventana,
        text=datos["nombre"],
        font=("Arial", 18, "bold")
    )

    lbl_nombre.pack(
        pady=10
    )

    if datos["imagen"]:

        headers = {
            "User-Agent":
            "ProyectoFamosos/1.0"
        }

        respuesta = requests.get(
            datos["imagen"],
            headers=headers
        )

        print("URL:")
        print(datos["imagen"])

        print("STATUS:")
        print(respuesta.status_code)

        print("TIPO:")
        print(
            respuesta.headers.get(
                "Content-Type"
            )
        )

        if respuesta.status_code == 200 and \
        "image" in respuesta.headers.get(
            "Content-Type",
            ""
        ):

            imagen = Image.open(
                BytesIO(
                    respuesta.content
                )
            )

        else:

            lbl_error = tk.Label(
                ventana,
                text=
                "No fue posible cargar la imagen.\n"
                "Wikipedia limitó las consultas."
            )

            lbl_error.pack(
                pady=20
            )

            return

        imagen.thumbnail(
            (300, 300)
        )

        foto = ImageTk.PhotoImage(
            imagen
        )

        lbl_imagen = tk.Label(
            ventana,
            image=foto
        )

        lbl_imagen.image = foto

        lbl_imagen.pack(
            pady=10
        )

    else:

        lbl_sin_imagen = tk.Label(
            ventana,
            text="Imagen no disponible"
        )

        lbl_sin_imagen.pack(
            pady=20
        )

    lbl_desc = tk.Label(
        ventana,
        text=datos["descripcion"],
        wraplength=500,
        justify="left"
    )

    lbl_desc.pack(
        padx=20,
        pady=10
    )

    lbl_fuente = tk.Label(
        ventana,
        text=
        f"Fuente: {datos['fuente']}",
        wraplength=500
    )

    lbl_fuente.pack(
        pady=10
    )

    lbl_fecha = tk.Label(
        ventana,
        text=
        f"Consulta API: {datos['fecha_consulta']}"
    )

    lbl_fecha.pack(
        pady=5
    )

if __name__ == "__main__":

    from api_wikipedia import (
        obtener_datos_famoso
    )

    datos = obtener_datos_famoso(
        "Madonna"
    )

    mostrar_famoso(
        datos
    )