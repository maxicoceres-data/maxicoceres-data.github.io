from git import Repo
import os
import streamlit as st

MAX_GITHUB_FILE_SIZE_BYTES = 100 * 1024 * 1024


def _archivos_grandes_trackeados(repo):
    grandes = []
    for item in repo.index.entries:
        ruta_relativa = item[0]
        ruta_absoluta = os.path.join(repo.working_tree_dir, ruta_relativa)
        if os.path.exists(ruta_absoluta):
            size_bytes = os.path.getsize(ruta_absoluta)
            if size_bytes > MAX_GITHUB_FILE_SIZE_BYTES:
                grandes.append((ruta_relativa, size_bytes))
    return grandes

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

        # 2. Commit SOLO si hay cambios locales reales.
        if repo.is_dirty(untracked_files=True):
            repo.git.add(A=True)

            archivos_grandes = _archivos_grandes_trackeados(repo)
            if archivos_grandes:
                listado = "\n".join(
                    f"- {ruta} ({size / (1024 * 1024):.2f} MB)" for ruta, size in archivos_grandes
                )
                st.error(
                    "No se puede sincronizar porque hay archivos mayores a 100 MB en git:\n"
                    f"{listado}\n"
                    "Reduce/comprime el archivo y vuelve a intentar."
                )
                return

            repo.index.commit("Actualización automática desde mi App.")
            st.info("Cambios locales detectados y commiteados.")
        else:
            st.info("No hay cambios locales nuevos. Se intentará push igualmente.")

        # 3. Pull con rebase y autostash para integrar cambios remotos sin romper el flujo.
        try:
            repo.git.pull('origin', rama_actual, '--rebase', '--autostash')
        except Exception as pull_error:
            st.error(f"Fallo al integrar cambios remotos (pull --rebase): {pull_error}")
            return

        # 4. Push explícito de la rama actual al remoto.
        try:
            resultado_push = origen.push(refspec=f"{rama_actual}:{rama_actual}")
            hubo_error = any(info.flags & info.ERROR for info in resultado_push)

            if hubo_error:
                detalle = "; ".join(info.summary for info in resultado_push)
                # Intentamos obtener detalle completo del remoto para identificar el motivo real.
                try:
                    salida_push = repo.git.push('origin', f"{rama_actual}:{rama_actual}")
                    st.error(f"Push rechazado: {detalle}. Detalle remoto: {salida_push}")
                except Exception as push_cli_error:
                    st.error(f"Push rechazado: {detalle}. Detalle remoto: {push_cli_error}")
                return

            st.success("Todo sincronizado en GitHub. Ya puedes hacer pull en VS Code.")
        except Exception as push_error:
            st.error(f"Fallo al subir a GitHub: {push_error}")

    except Exception as e:
        st.error(f"Error general: {e}")