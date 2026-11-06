import requests

BASE = "https://localhost:8443"

# Forma correcta: verificando contra nuestro certificado.pem
r1 = requests.get(f"{BASE}/incidencias", verify="certificado.pem", timeout=10)
print("Con certificado.pem (Seguro):", r1.status_code, r1.json())

# Mala práctica: apagando la verificación (lanza InsecureRequestWarning)
r2 = requests.get(f"{BASE}/incidencias", verify=False, timeout=10)
print("Con verify=False (Inseguro):", r2.status_code, r2.json())