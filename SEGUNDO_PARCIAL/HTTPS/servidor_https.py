import http.server, json, time, ssl
from urllib.parse import urlparse, parse_qs

ARCHIVO = "incidencias.json"
ESTADOS = ("abierta", "en_proceso", "resuelta")
siguiente_id = 1

def cargar():
    global siguiente_id
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            datos = json.load(f)
            if datos: siguiente_id = max(i["id"] for i in datos) + 1
            return datos
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(incidencias, f, ensure_ascii=False, indent=2)

incidencias = cargar()
logs = []
contadores = {
    "peticiones_totales": 0,
    "por_metodo": {"GET": 0, "POST": 0, "PATCH": 0, "PUT": 0, "DELETE": 0, "HEAD": 0},
    "por_familia": {"2xx": 0, "4xx": 0, "5xx": 0},
    "incidencias_por_tipo": {"alerta": 0, "vulnerabilidad": 0, "incidente": 0},
}

class Manejador(http.server.BaseHTTPRequestHandler):
    def _leer_json(self):
        try:
            tam = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(tam).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            return None

    def _enviar(self, codigo, datos=None):
        cuerpo = b"" if datos is None else json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        if self.command != "HEAD": self.wfile.write(cuerpo)
        logs.append({"hora": time.strftime("%H:%M:%S"), "metodo": self.command, "ruta": self.path, "codigo": codigo})
        contadores["peticiones_totales"] += 1
        contadores["por_metodo"][self.command] = contadores["por_metodo"].get(self.command, 0) + 1
        contadores["por_familia"][f"{codigo // 100}xx"] += 1

    def _obtener_id(self, ruta):
        if not ruta.startswith("/incidencias/"):
            self._enviar(404, {"error": f"ruta no conocida: {ruta}"})
            return None
        try:
            return int(ruta.split("/")[2])
        except ValueError:
            self._enviar(400, {"error": "id debe ser entero"})
            return None

    def do_HEAD(self):
        url = urlparse(self.path)
        self._enviar(200 if url.path in ("/", "/incidencias", "/logs", "/contadores") else 404)

    def do_GET(self):
        url, params = urlparse(self.path), parse_qs(urlparse(self.path).query)
        if url.path == "/":
            self._enviar(200, {"servicio": "Bitácora de incidencias HTTPS", "rutas": ["GET /incidencias", "GET /incidencias/<id>", "POST /incidencias", "PATCH /incidencias/<id>", "PUT /incidencias/<id>", "DELETE /incidencias/<id>", "GET /logs", "GET /contadores"]})
        elif url.path == "/incidencias":
            lista = [i for i in incidencias if ("tipo" not in params or i["tipo"] == params["tipo"][0]) and ("estado" not in params or i["estado"] == params["estado"][0])]
            self._enviar(200, lista)
        elif url.path == "/logs": self._enviar(200, logs)
        elif url.path == "/contadores": self._enviar(200, contadores)
        else:
            buscado = self._obtener_id(url.path)
            if buscado is not None:
                inc = next((i for i in incidencias if i["id"] == buscado), None)
                self._enviar(200, inc) if inc else self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def do_POST(self):
        if urlparse(self.path).path != "/incidencias": return self._enviar(404, {"error": f"ruta no conocida: {self.path}"})
        datos = self._leer_json()
        if not isinstance(datos, dict): return self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
        faltan = [c for c in ("tipo", "descripcion") if c not in datos]
        if faltan: return self._enviar(400, {"error": f"faltan campos: {', '.join(faltan)}"})
        estado = str(datos.get("estado", "abierta"))
        if estado not in ESTADOS: return self._enviar(400, {"error": f"estado inválido. Válidos: {', '.join(ESTADOS)}"})
        global siguiente_id
        inc = {"id": siguiente_id, "tipo": str(datos["tipo"]), "descripcion": str(datos["descripcion"]), "estado": estado, "hora": time.strftime("%Y-%m-%d %H:%M:%S")}
        siguiente_id += 1
        incidencias.append(inc)
        contadores["incidencias_por_tipo"][inc["tipo"]] = contadores["incidencias_por_tipo"].get(inc["tipo"], 0) + 1
        guardar()
        self._enviar(201, inc)

    def do_PATCH(self):
        buscado = self._obtener_id(urlparse(self.path).path)
        if buscado is None: return
        datos = self._leer_json()
        if not isinstance(datos, dict): return self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
        if "estado" in datos and str(datos["estado"]) not in ESTADOS: return self._enviar(400, {"error": f"estado inválido. Válidos: {', '.join(ESTADOS)}"})
        for inc in incidencias:
            if inc["id"] == buscado:
                for c in ("tipo", "descripcion", "estado"):
                    if c in datos: inc[c] = str(datos[c])
                guardar()
                return self._enviar(200, inc)
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def do_PUT(self):
        buscado = self._obtener_id(urlparse(self.path).path)
        if buscado is None: return
        datos = self._leer_json()
        if not isinstance(datos, dict): return self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
        faltan = [c for c in ("tipo", "descripcion") if c not in datos]
        if faltan: return self._enviar(400, {"error": f"faltan campos: {', '.join(faltan)}"})
        for i, inc in enumerate(incidencias):
            if inc["id"] == buscado:
                incidencias[i] = {"id": buscado, "tipo": str(datos["tipo"]), "descripcion": str(datos["descripcion"]), "estado": "abierta", "hora": time.strftime("%Y-%m-%d %H:%M:%S")}
                guardar()
                return self._enviar(200, incidencias[i])
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def do_DELETE(self):
        buscado = self._obtener_id(urlparse(self.path).path)
        if buscado is None: return
        for i, inc in enumerate(incidencias):
            if inc["id"] == buscado:
                del incidencias[i]
                guardar()
                return self._enviar(204)
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def log_message(self, formato, *args): pass

contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
contexto.load_cert_chain("certificado.pem", "llave.pem")

servidor = http.server.HTTPServer(("localhost", 8443), Manejador)
servidor.socket = contexto.wrap_socket(servidor.socket, server_side=True)
print("Bitácora HTTPS en https://localhost:8443")
servidor.serve_forever()