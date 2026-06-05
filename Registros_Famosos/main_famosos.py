import tkinter as tk
import pandas as pd
from tkinter import filedialog
from procesador_famosos import (
    procesar_famosos
)

from api_wikipedia import (
    obtener_datos_famoso
)

from visor_famosos import (
    mostrar_famoso
)

ventana = tk.Tk()

ventana.title(
    "Famosos"
)

ventana.geometry(
    "500x400"
)

titulo = tk.Label(
    ventana,
    text="Listado de Famosos",
    font=("Arial", 16)
)

titulo.pack(
    pady=10
)

lista = tk.Listbox(
    ventana,
    width=50,
    height=10
)

lista.pack(
    pady=10
)

def ver_informacion():

    seleccion = lista.curselection()

    if not seleccion:

        return

    indice = seleccion[0]

    nombre = (
        df.iloc[indice]["NOMBRE"]
        .title()
    )

    datos = obtener_datos_famoso(
        nombre
    )

    print(datos)
    
    mostrar_famoso(
        datos
    )


btn_ver = tk.Button(
    ventana,
    text="Ver información",
    command=ver_informacion,
    width=20
)

btn_ver.pack(
    pady=10
)

def cargar_archivo():

    ruta = filedialog.askopenfilename(
        title="Seleccionar CSV",
        filetypes=[
            ("CSV", "*.csv")
        ]
    )

    if not ruta:
        return

    procesar_famosos(
        ruta
    )

    cargar_lista()

btn_cargar = tk.Button(
    ventana,
    text="Cargar CSV",
    command=cargar_archivo,
    width=20
)

btn_cargar.pack(
    pady=10
)

def cargar_lista():

    global df

    lista.delete(
        0,
        tk.END
    )

    df = pd.read_csv(
        "outputs/famosos_consolidados.csv"
    )

    for _, fila in df.iterrows():

        lista.insert(
            tk.END,
            f"{fila['NOMBRE']} - {fila['EDAD']} años"
        )

ventana.mainloop()