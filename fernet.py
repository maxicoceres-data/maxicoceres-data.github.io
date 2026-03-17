from cryptography.fernet import Fernet
key = Fernet.generate_key().decode()
print(key)
# Esto te dará algo como: 45JkLp... (CÓPIALO)