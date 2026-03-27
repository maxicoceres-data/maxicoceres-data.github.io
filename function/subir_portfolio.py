from git import Repo
import os
import streamlit as st

def subir_portfolio():
    try:
        if "GITHUB_TOKEN" not in st.secrets:
            st.error("Falta GITHUB_TOKEN en secrets. No se puede sincronizar.")
            return

        TOKEN = st.secrets["GITHUB_TOKEN"]
        ruta_repo = os.path.dirname(os.path.abspath(__file__))
        ruta_proy = os.path.abspath(os.path.join(ruta_repo, ".."))

        repo = Repo(ruta_proy)
        rama_actual = repo.active_branch.name

        # 1. Aseguramos el REMOTO con el TOKEN
        remote_url = f"https://x-access-token:{TOKEN}@github.com/maxicoceres-data/maxicoceres-data.github.io.git"
        if 'origin' in repo.remotes:
            origen = repo.remote(name='origin')
            origen.set_url(remote_url)
        else:
            origen = repo.create_remote('origin', remote_url)

        # 2. Sincronizamos antes de commitear para evitar conflictos de historia.
        try:
            repo.git.pull('origin', rama_actual, rebase=True)
        except Exception as pull_error:
            st.warning(f"No se pudo hacer pull previo: {pull_error}")

        # 3. Commit SOLO si hay cambios locales reales.
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)
            repo.index.commit("Actualización automática desde mi App.")
            st.info("Cambios locales detectados y commiteados.")
        else:
            st.info("No hay cambios locales nuevos. Se intentará push igualmente.")

        # 4. Push explícito de la rama actual al remoto.
        try:
            resultado_push = origen.push(refspec=f"{rama_actual}:{rama_actual}")
            hubo_error = any(info.flags & info.ERROR for info in resultado_push)

            if hubo_error:
                detalle = "; ".join(info.summary for info in resultado_push)
                st.error(f"Push con error: {detalle}")
                return

            st.success("Todo sincronizado en GitHub. Ya puedes hacer pull en VS Code.")
        except Exception as push_error:
            st.error(f"Fallo al subir a GitHub: {push_error}")

    except Exception as e:
        st.error(f"Error general: {e}")