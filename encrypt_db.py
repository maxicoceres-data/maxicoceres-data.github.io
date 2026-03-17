# encrypt_db.py
from cryptography.fernet import Fernet

def encrypt_file(in_path: str, out_path: str, key: bytes):
    f = Fernet(key)
    with open(in_path, 'rb') as r:
        data = r.read()
    token = f.encrypt(data)
    with open(out_path, 'wb') as w:
        w.write(token)

if __name__ == "__main__":
    import sys, os
    key = os.environ.get('FERNET')
    if not key:
        raise SystemExit("Set FERNET env var before running")
    encrypt_file("mi_base.db", "mi_base.db.enc", key.encode())