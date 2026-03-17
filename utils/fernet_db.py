import os
import tempfile
import atexit
from cryptography.fernet import Fernet


def decrypt_db_to_temp(enc_path: str) -> str:
    """Descifra `enc_path` usando la clave FERNET encontrada en Streamlit secrets
    o en la variable de entorno `FERNET`. Devuelve la ruta a un archivo temporal
    .db que debe existir mientras la app esté en ejecución.
    """
    # Intentar leer la clave desde streamlit secrets si está disponible
    key = None
    try:
        import streamlit as st
        key = st.secrets.get("FERNET") or os.environ.get("FERNET")
    except Exception:
        key = os.environ.get("FERNET")

    if not key:
        raise RuntimeError("FERNET key not found in Streamlit secrets or environment")

    with open(enc_path, "rb") as f:
        token = f.read()

    data = Fernet(key.encode()).decrypt(token)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    tmp.write(data)
    tmp.flush()
    tmp.close()

    def _cleanup(path=tmp.name):
        try:
            os.remove(path)
        except Exception:
            pass

    atexit.register(_cleanup)
    return tmp.name
