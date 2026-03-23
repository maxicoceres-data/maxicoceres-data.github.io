import streamlit as st


def login(usuario_ingresado, clave_ingresada, usuario_db, clave_db):
    
    
    if usuario_ingresado == usuario_db and clave_ingresada == clave_db:
        st.session_state["autenticado"] = True
        st.success("Acceso concedido")
        st.rerun()
    else:
        st.error("Usuario / Contraseña incorrecta")
  
    
