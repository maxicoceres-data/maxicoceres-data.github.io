from git import Repo
import os
import streamlit as st

def subir_portfolio():
    try:
        
        TOKEN = st.secrets["GITHUB_TOKEN"]
        ruta_repo = os.path.dirname(os.path.abspath(__file__))
        
        ruta_proy = os.path.abspath(os.path.join(ruta_repo, ".."))
        
        repo = Repo(ruta_proy)
        
        with repo.config_writer() as cw:
            cw.set_value("user","name","maxicoceres-data")
            cw.set_value("user","email","maximiliano.g.coceres@gmail.com")
        
        repo.git.add(A=True)
        
        
        repo.git.commit(m="Actualización automatica desde mi App.")
        
        remote_url = f"https://{TOKEN}@github.com/maxicoceres-data/maxicoceres-data.github.io.git"

        if 'origin' in repo.remotes:
            repo.remote(name='origin').set_url(remote_url)
        
        origen = repo.remote(name='origin')
        origen.push()
        
        st.success("Portfolio actualizado con exito!")
        
        
    except Exception as e:
        st.warning(f"Error: {e}")