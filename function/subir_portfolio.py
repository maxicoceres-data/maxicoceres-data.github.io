from git import Repo
import os
import streamlit as st

def subir_portfolio():
    try:
        ruta_repo = os.path.dirname(os.path.abspath(__file__))
        
        ruta_proy = os.path.abspath(os.path.join(ruta_repo, ".."))
        
        repo = Repo(ruta_proy)
        
        repo.git.add(A=True)
        
        
        repo.git.commit(m="Actualización automatica desde mi App.")
        
        origen = repo.remote(name='origin')
        origen.push()
        
        st.success("Portfolio actualizado con exito!")
        
        
    except Exception as e:
        st.warning(f"Error: {e}")