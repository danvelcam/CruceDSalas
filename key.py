from Crypto.Random import get_random_bytes
import base64

# Generar una clave AES de 256 bits (32 bytes)
key = get_random_bytes(32)

# Convertir la clave a una cadena base64 para almacenarla fácilmente
key_base64 = base64.b64encode(key).decode()

# Guardar la clave en un archivo .env
with open(".env", "a") as env_file:
    env_file.write(f"AES_KEY={key_base64}\n")

print(f"Generated AES Key: {key_base64}")