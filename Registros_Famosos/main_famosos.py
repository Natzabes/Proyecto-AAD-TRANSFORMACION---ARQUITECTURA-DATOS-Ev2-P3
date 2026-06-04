import tkinter as tk
import pandas as pd
import os
from api_wikipedia import obtener_datos_famoso
from visor_famosos import mostrar_famoso
from procesador_famosos import procesar_famosos

# Asegurar que el archivo consolidado exista al arrancar
ruta_origen = "famosos.csv" # Tu CSV original con los nombres y fechas
ruta_salida = "outputs/famosos_consolidados.csv"

if not os.path.exists(ruta_salida):
    print("Procesando datos por primera vez...")
    procesar_famosos(ruta_origen)

ventana = tk.Tk()
ventana.title("Famosos")
ventana.geometry("500x450")

titulo = tk.Label(ventana, text="Listado de Famosos", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

try:
    df = pd.read_csv(ruta_salida)
except Exception as e:
    df = pd.DataFrame(columns=["NOMBRE", "EDAD"])
    print(f"Error cargando archivo consolidado: {e}")

lista = tk.Listbox(ventana, width=50, height=12)

for _, fila in df.iterrows():
    lista.insert(tk.END, f"{fila['NOMBRE']} - {fila['EDAD']} años")

lista.pack(pady=10)

def ver_informacion():
    seleccion = lista.curselection()
    if not seleccion:
        return

    indice = seleccion[0]
    nombre = df.iloc[indice]["NOMBRE"]

    datos = obtener_datos_famoso(nombre)
    mostrar_famoso(datos)

btn_ver = tk.Button(ventana, text="Ver información", command=ver_informacion, width=20, bg="lightgreen")
btn_ver.pack(pady=10)

ventana.mainloop()