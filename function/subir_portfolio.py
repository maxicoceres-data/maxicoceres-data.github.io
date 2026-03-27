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

        
        # 2. Intentar hacer Commit SOLO si hay cambios
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit("Actualización automática desde mi App.")
            st.info("✅ Cambios locales guardados (Commit realizado).")
        else:
            st.info("ℹ️ No hay cambios pendientes, procediendo a subir lo acumulado...")

        # 3. EL PASO CLAVE: Forzar el Push aunque no haya habido commit nuevo ahora
        # Usamos un try/except específico para el push
        try:
            # Hacemos un pull con rebase por si acaso alguien tocó algo en GitHub
            repo.git.pull('origin', 'main', rebase=True)
            
            # Subimos los commits que están "adelantados"
            origen.push()
            st.success("🚀 ¡TODO SINCRONIZADO! Ya puedes hacer 'git pull' en tu VS Code.")
        except Exception as push_error:
            st.error(f"Fallo al subir a GitHub: {push_error}")

    except Exception as e:
        st.error(f"Error general: {e}")