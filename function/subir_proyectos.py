import sqlite3
import streamlit as st
from function.path import path_ubicacion

def subir_proyecto(titulo= None,cant_tecnologia= None,tecnologia= None,descripcion= None,url= None,github= None):
    
    DB_PATH= path_ubicacion()
    
    
    # Validaciones
    if not all([titulo, cant_tecnologia, tecnologia, descripcion, url, github]):
        st.error("Faltan campos obligatorios.")
        return
    
    try:
        cant = int(cant_tecnologia)
    except Exception:
        st.error("Cantidad de tecnologías inválida.")
        return
    
    tecnologias_string = tecnologia if isinstance(tecnologia, str) else ",".join(map(str, tecnologia))
    
    if not url.lower().endswith((".png", ".mp4")):
        st.error("El archivo tiene que ser .png o .mp4.")
        return

    if not github.lower().startswith("https://github.com/maxicoceres-data/"):
        st.error("La URL de GitHub debe comenzar con https://github.com/maxicoceres-data/")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proyectos (titulo,tecnologia,descripcion,url,github) VALUES (?,?,?,?,?)", (titulo,tecnologias_string,descripcion,url,github))
        
        conn.commit()
    except Exception as e:
        st.error(f'Error al subir proyecto: {e}')
    finally:
        try:
            conn.close()
        except:
            pass
    