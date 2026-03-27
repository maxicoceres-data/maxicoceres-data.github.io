from git import Repo
import os
import streamlit as st

def subir_portfolio():
    try:
        
        TOKEN = st.secrets["GITHUB_TOKEN"]
        ruta_repo = os.path.dirname(os.path.abspath(__file__))
        
        ruta_proy = os.path.abspath(os.path.join(ruta_repo, ".."))
        
        repo = Repo(ruta_proy)
        
        # 1. Aseguramos el REMOTO con el TOKEN
        remote_url = f"https://{TOKEN}@github.com/maxicoceres-data/maxicoceres-data.github.io.git"
        if 'origin' in repo.remotes:
            origen = repo.remote(name='origin')
            origen.set_url(remote_url)
        else:
            origen = repo.create_remote('origin', remote_url)

        
        # 2. Sincronizamos (Traemos lo que hay en GitHub)
        try:
            origen.pull() 
        except Exception:
            pass

        # 3. Agregamos y Comiteamos
        repo.git.add(A=True)
        
        # Solo hacemos commit si hay cambios reales para evitar el error de "nothing to commit"
        if repo.is_dirty(untracked_files=True):
            repo.index.commit("Actualización automatica desde mi App.")

            origen.push()
            st.success("🚀 ¡Portfolio actualizado con éxito!")
        else:
            st.info("ℹ️ No hay cambios nuevos para subir.")

    except Exception as e:
        st.error(f"❌ Error crítico: {e}")