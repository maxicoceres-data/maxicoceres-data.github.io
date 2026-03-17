import streamlit as st
from function.subir_proyectos import subir_proyecto
from function.eliminar_proyecto import eliminar_proyecto
from function.modificar_proyecto import modificar_proyecto
from function.generar_web import generar_web
from function.subir_portfolio import subir_portfolio
from function.path import path_ubicacion
import pandas as pd
import sqlite3

# Intentar usar la versión cifrada de la DB si existe (mi_base.db.enc)
DB_PATH = path_ubicacion()


conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM proyectos", conn)

st.title("Panel de proyectos")

herramientas = st.sidebar.radio("Herramientas", ["Nuevo Proyecto", "Modificar Proyecto", "Eliminar Proyecto"])
st.sidebar.divider()
st.sidebar.caption("📂 Preparación")
button_carga = st.sidebar.button("Analizar Cambios")
st.sidebar.write("⬇️")
st.sidebar.caption("🌍 Subir web")
button_subir = st.sidebar.button("Sincronizar Portfolio")
if button_carga:
    @st.dialog("¿Desea cargar el proyecto?")
    def mostrar_mensaje_cargar():
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cargar"):
                generar_web()
        with col2:
            if st.button("Cerrar"):
                st.rerun()
    mostrar_mensaje_cargar()

if button_subir:
    @st.dialog("¿Desea subir el portfolio?")
    def mostrar_mensaje_subir():
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Subir"):
                subir_portfolio()
        with col2:
            if st.button("Cerrar"):
                st.rerun()
    mostrar_mensaje_subir()

st.sidebar.link_button("Ver Portfolio","https://maxicoceres-data.github.io",)

if herramientas == "Nuevo Proyecto":
    with st.form("Carga de nuevo proyecto: "):
        titulo = st.text_input("Título del proyecto")
        cantidad = st.number_input("Cantidad de tecnologias", placeholder= "Escribe la cantidad", step=1)
        tecnologias = st.text_input("Tecnologias",placeholder="Para muchas tecnologias, escribilas seguidas de ',' ")
        descripcion = st.text_area("Descripción", placeholder="Añade una descripción del proyecto")
        url = st.text_input("Url del video o imagen", placeholder="Añadir el url del video o imagen. Ej. imagen.png o video.mp4", help="La imagen tiene que ser PNG y el video MP4")
        github = st.text_input("Url del github", value= "https://github.com/maxicoceres-data/",placeholder="Añadir url del github", help="Tiene que comenzar con https://github.com/maxicoceres-data/")
        
        button = st.form_submit_button("Subir Proyecto")
        
        if button:
            subir_proyecto(
                titulo=titulo,
                cant_tecnologia=cantidad,
                tecnologia=tecnologias,
                descripcion=descripcion,
                url=url,
                github=github
            )
            st.success("¡Proyecto subido correctamente!")
            
elif herramientas == "Eliminar Proyecto":
    with st.form("Eliminar Proyecto por ID"):
        numero_id = st.number_input("ID del proyecto", placeholder= "Escribe el ID del proyecto a eliminar", step=1)
        button_eliminar = st.form_submit_button("Eliminar Proyecto")
        
        st.dataframe(df)
        
        if button_eliminar:
            @st.dialog(f"Estas seguro de eliminar el proyecto: {numero_id}?")
            def mostrar_confirmacion():
                col1,col2 = st.columns(2)
                with col1:
                    if st.button("Borrar"):
                        eliminar_proyecto(id_eliminar=numero_id)
                with col2:
                    if st.button("Cerrar"):
                        st.rerun()
            mostrar_confirmacion()
            
                
elif herramientas == "Modificar Proyecto":
    with st.form("Modificar datos del proyecto"):
        columna = st.text_input("Columna a modificar", placeholder="Escribe el nombre de la columna")
        id_proyecto = st.number_input("Número del Proyecto (Numero ID)",step=1)
        valor = st.text_area("Texto a modificar", placeholder="Escribe el nuevo valor a modificar", help="Si son tecnologias, escribilas seguidas de ','")
        button_modificar = st.form_submit_button("Modificar Proyecto")
        
        st.dataframe(df)
        
        
        @st.dialog(f"Estas seguro de modificar el proyecto: {id_proyecto}?")
        def mensaje_proyecto_modificado():
            st.success("Proyecto Modificado")
            if st.button("Cerrar"):
                st.rerun()
        
        if button_modificar:
            @st.dialog(f"Estas seguro de modificar el proyecto: {id_proyecto}?")
            def mensaje_proyecto_modificado():
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Modificar"):
                        modificar_proyecto(
                            col = columna,
                            id_modificar=id_proyecto,
                            valor=valor
                        )
                with col2:
                    if st.button("Cerrar"):
                        st.rerun()
            mensaje_proyecto_modificado()
            
        
        