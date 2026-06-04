import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def mostrar_famoso(datos):
    if not datos:
        return

    ventana = tk.Toplevel()
    ventana.title(datos["nombre"])
    ventana.geometry("600x750")

    lbl_nombre = tk.Label(ventana, text=datos["nombre"], font=("Arial", 18, "bold"))
    lbl_nombre.pack(pady=10)

    # Validación de la existencia de la imagen
    if datos["imagen"]:
        try:
            headers = {"User-Agent": "ProyectoFamosos/1.0"}
            respuesta = requests.get(datos["imagen"], headers=headers)
            imagen = Image.open(BytesIO(respuesta.content))
        except Exception as e:
            print(f"No se pudo cargar la imagen de internet: {e}")
            imagen = Image.new('RGB', (300, 300), color='gray') # Imagen gris por defecto
    else:
        # Si la API no devolvió imagen (ej. Julio César antiguo)
        imagen = Image.new('RGB', (300, 300), color='gray')

    # Escalado correcto (proporcional gracias a thumbnail)
    imagen.thumbnail((300, 300))
    foto = ImageTk.PhotoImage(imagen)

    lbl_imagen = tk.Label(ventana, image=foto)
    lbl_imagen.image = foto
    lbl_imagen.pack(pady=10)

    lbl_desc = tk.Label(ventana, text=datos["descripcion"], wraplength=500, justify="left")
    lbl_desc.pack(padx=20, pady=10)

    # Mostrar Fuente y Captura requeridas
    lbl_fuente = tk.Label(ventana, text=f"Fuente: {datos['fuente']}", wraplength=500, fg="blue")
    lbl_fuente.pack(pady=2)

    lbl_captura = tk.Label(ventana, text=f"Captura: {datos['captura']}", font=("Arial", 10, "italic"))
    lbl_captura.pack(pady=5)