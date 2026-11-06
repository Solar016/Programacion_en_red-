import requests

BASE = "http://localhost:8001"

# 1. Crear 3 incidencias (POST)
r1 = requests.post(f"{BASE}/incidencias", json={"tipo": "alerta", "descripcion": "Escaneo de puertos"}, timeout=10)
r2 = requests.post(f"{BASE}/incidencias", json={"tipo": "vulnerabilidad", "descripcion": "SSH con contrasena debil"}, timeout=10)
r3 = requests.post(f"{BASE}/incidencias", json={"tipo": "incidente", "descripcion": "Intento de acceso no autorizado"}, timeout=10)
id_editar = r1.json()["id"]
id_borrar = r3.json()["id"]
print("POST creadas:", r1.status_code, r2.status_code, r3.status_code)

# 2. Consultar con filtros combinados (GET - Ejercicio 5)
for filtro in [{"tipo": "alerta"}, {"estado": "abierta"}, {"tipo": "alerta", "estado": "abierta"}]:
    r = requests.get(f"{BASE}/incidencias", params=filtro, timeout=10)
    print(f"GET {filtro}:", len(r.json()), "resultado(s)")

# 3. Modificar estado válido e inválido (PATCH - Ejercicio 1)
print("PATCH valido:", requests.patch(f"{BASE}/incidencias/{id_editar}", json={"estado": "en_proceso"}, timeout=10).status_code)
print("PATCH invalido (400):", requests.patch(f"{BASE}/incidencias/{id_editar}", json={"estado": "otro"}, timeout=10).status_code)

# 4. Reemplazo completo (PUT - Ejercicio 4)
print("PUT reemplazo:", requests.put(f"{BASE}/incidencias/{id_editar}", json={"tipo": "alerta", "descripcion": "Escaneo de puertos bloqueado"}, timeout=10).status_code)

# 5. Comprobar error 404
r_404 = requests.get(f"{BASE}/incidencias/999", timeout=10)
if r_404.status_code == 404:
    print("404 verificado:", r_404.json()["error"])

# 6. Eliminar solo la tercera incidencia (DELETE) para dejar 2 guardadas en disco
print("DELETE borrar una:", requests.delete(f"{BASE}/incidencias/{id_borrar}", timeout=10).status_code)

# 7. Auditoría del servidor (/contadores y /logs)
print("Contadores:", requests.get(f"{BASE}/contadores", timeout=10).json())
print("Total logs:", len(requests.get(f"{BASE}/logs", timeout=10).json()))