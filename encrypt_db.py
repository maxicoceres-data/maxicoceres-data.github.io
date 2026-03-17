from cryptography.fernet import Fernet
import os
from function.path import path_ubicacion


def encrypt_file(in_path: str, out_path: str, key: bytes):
    f = Fernet(key)
    with open(in_path, 'rb') as r:
        data = r.read()
    token = f.encrypt(data)
    with open(out_path, 'wb') as w:
        w.write(token)


if __name__ == "__main__":
    # Leer clave desde variable de entorno FERNET
    key = os.environ.get('FERNET')
    if not key:
        raise SystemExit("Set FERNET env var before running (export FERNET=...)")

    # Obtener la ruta real de la DB (function.path.path_ubicacion retorna Path)
    db_path = path_ubicacion()
    db_path_str = str(db_path)
    enc_path = db_path_str + ".enc"

    if not os.path.exists(db_path_str):
        raise SystemExit(f"DB file not found: {db_path_str}")

    encrypt_file(db_path_str, enc_path, key.encode())
    print(f"Encrypted {db_path_str} -> {enc_path}")