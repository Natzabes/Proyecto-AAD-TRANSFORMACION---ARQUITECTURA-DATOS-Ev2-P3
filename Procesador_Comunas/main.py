import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from procesador_comunas import (
    procesar_archivo_comunas,
    limpiar_comparacion,
    buscar_sugerencias
)

ventana = tk.Tk()

ventana.title(
    "Procesador de Comunas"
)

ventana.geometry(
    "500x300"
)

formato_var = tk.StringVar(
    value="titulo"
)

titulo = tk.Label(
    ventana,
    text="Procesador de Comunas",
    font=("Arial", 16)
)

titulo.pack(pady=10)

lbl_formato = tk.Label(
    ventana,
    text="Seleccione formato:"
)

lbl_formato.pack()

rb1 = tk.Radiobutton(
    ventana,
    text="MAYÚSCULAS",
    variable=formato_var,
    value="mayusculas"
)

rb1.pack()

rb2 = tk.Radiobutton(
    ventana,
    text="minúsculas",
    variable=formato_var,
    value="minusculas"
)

rb2.pack()

rb3 = tk.Radiobutton(
    ventana,
    text="Título",
    variable=formato_var,
    value="titulo"
)

rb3.pack()

def cargar_archivo():

    ruta = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[
            (
                "Archivos compatibles",
                "*.csv *.txt *.xlsx"
            )
        ]
    )

    if not ruta:
        return

    formato = formato_var.get()

    procesar_archivo_comunas(
        ruta,
        formato
    )

    messagebox.showinfo(
        "Proceso terminado",
        "Archivo procesado correctamente."
    )

def buscar_comuna():

    ventana_busqueda = tk.Toplevel(
        ventana
    )

    ventana_busqueda.title(
        "Buscar Comuna"
    )

    ventana_busqueda.geometry(
        "450x300"
    )

    lbl = tk.Label(
        ventana_busqueda,
        text="Ingrese una comuna:"
    )

    lbl.pack(
        pady=10
    )

    entrada_comuna = tk.Entry(
        ventana_busqueda,
        width=30
    )

    entrada_comuna.pack(
        pady=5
    )

    resultado_label = tk.Label(
        ventana_busqueda,
        text="",
        justify="left"
    )

    resultado_label.pack(
        pady=10
    )

    def ejecutar_busqueda():

        comuna = entrada_comuna.get()

        comuna_comparacion = (
            limpiar_comparacion(comuna)
        )

        df = pd.read_csv(
            "data/Poblacion-Comunas-de-Chie-INE-2015-2020.csv"
        )

        df["COMPARACION"] = (
            df["COMUNA"]
            .apply(limpiar_comparacion)
        )

        resultado = df[
            df["COMPARACION"]
            == comuna_comparacion
        ]

        lista_comunas = (
            df["COMPARACION"]
            .tolist()
        )

        if not resultado.empty:

            comuna_real = (
                resultado.iloc[0]["COMUNA"]
            )

            region = (
                resultado.iloc[0]["REGION"]
            )

            habitantes = (
                resultado.iloc[0]["HABITANTES"]
            )

            resultado_label.config(
                text=
                f"Comuna: {comuna_real}\n"
                f"Región: {region}\n"
                f"Habitantes: {habitantes}"
            )

        else:

            sugerencias = buscar_sugerencias(
                comuna_comparacion,
                lista_comunas
            )

            if sugerencias:

                texto_sugerencias = (
                    "Comuna no encontrada\n\n"
                    "¿Quiso decir?\n"
                )

                for sugerencia in sugerencias:

                    nombre_real = df[
                        df["COMPARACION"]
                        == sugerencia
                    ].iloc[0]["COMUNA"]

                    texto_sugerencias += (
                        f"- {nombre_real}\n"
                    )

                resultado_label.config(
                    text=texto_sugerencias
                )

            else:

                resultado_label.config(
                    text=
                    "Comuna no encontrada"
                )

    def limpiar_busqueda():

        entrada_comuna.delete(
            0,
            tk.END
        )

        resultado_label.config(
            text=""
        )

        entrada_comuna.focus()

    btn_ejecutar = tk.Button(
        ventana_busqueda,
        text="Buscar",
        command=ejecutar_busqueda
    )

    btn_ejecutar.pack(
        pady=10
    )

    btn_limpiar = tk.Button(
        ventana_busqueda,
        text="Limpiar",
        command=limpiar_busqueda
    )

    btn_limpiar.pack(
        pady=5
    )

btn_cargar = tk.Button(
    ventana,
    text="Cargar archivo",
    command=cargar_archivo,
    width=25
)

btn_cargar.pack(
    pady=15
)

btn_buscar = tk.Button(
    ventana,
    text="Buscar comuna",
    command=buscar_comuna,
    width=25
)

btn_buscar.pack(
    pady=5
)

ventana.mainloop()
