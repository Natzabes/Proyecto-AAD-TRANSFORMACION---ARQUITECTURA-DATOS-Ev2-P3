import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Photon  # Cambiado a Photon para evitar bloqueos
from geopy.extra.rate_limiter import RateLimiter

# Configuración de la página
st.set_page_config(page_title="Mapa de Lugares", layout="wide")
st.title("🌍 Localizador de Destinos")

# 1. Cargar datos
try:
    df = pd.read_csv('lugares.csv')
    st.success("Archivo 'lugares.csv' cargado correctamente.")
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# 2. Geocodificación (Photon es más rápido y tiene menos restricciones de timeout)
geolocator = Photon(user_agent="my_map_application_2026")
# Aumentamos el delay a 1.5 segundos para ser respetuosos con el servidor
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

@st.cache_data
def get_coordinates(_lista_nombres):
    data = []
    # Usamos una barra de progreso nativa de Streamlit (sin spinners conflictivos)
    progreso = st.progress(0)
    total = len(_lista_nombres)
    
    for i, nombre in enumerate(_lista_nombres):
        try:
            # Añadimos un timeout explícito de 10 segundos para evitar cortes bruscos
            location = geolocator.geocode(nombre, timeout=10)
            if location:
                data.append({
                    "nombre": nombre,
                    "lat": location.latitude,
                    "lon": location.longitude
                })
        except Exception:
            # Si un lugar falla, se lo salta y continúa con el resto
            pass
        progreso.progress((i + 1) / total)
        
    progreso.empty()
    return pd.DataFrame(data)

st.info("Obteniendo coordenadas de los lugares... Por favor, espera.")
df_coords = get_coordinates(df['NOMBRE_LUGAR'].unique()) # .unique() evita buscar duplicados

# 3. Crear el mapa interactivo
m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df_coords.iterrows():
    # Enlace de Google Maps basado en coordenadas reales
    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
    
    # Ventana emergente con el enlace
    popup_html = f"""
        <div style="font-family: sans-serif; font-size: 14px;">
            <strong>{row['nombre']}</strong><br><br>
            <a href="{gmaps_url}" target="_blank" style="
                background-color: #4CAF50; 
                color: white; 
                padding: 5px 10px; 
                text-decoration: none; 
                border-radius: 4px;
                display: inline-block;">
                📍 Ver en Google Maps
            </a>
        </div>
    """
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=row['nombre']
    ).add_to(m)

# 4. Mostrar mapa
st_folium(m, width="100%", height=600)

st.subheader("Datos procesados con éxito:")
st.dataframe(df_coords)