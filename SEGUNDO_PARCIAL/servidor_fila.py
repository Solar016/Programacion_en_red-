from xmlrpc.server import SimpleXMLRPCServer
import threading

# Variables globales compartidas
contador_turnos = 0
lock_turnos = threading.Lock()

def tomar_turno(apodo):
    global contador_turnos
    with lock_turnos:
        contador_turnos += 1
        turno_asignado = contador_turnos
    
    print(f"Turno {turno_asignado} asignado a {apodo}")
    return turno_asignado

def cuantos_van():
    with lock_turnos:
        total = contador_turnos
    return total

if __name__ == "__main__":
    servidor = SimpleXMLRPCServer(("localhost", 5000))
    # Se exponen las funciones con un nombre público
    servidor.register_function(tomar_turno, "tomar_turno")
    servidor.register_function(cuantos_van, "cuantos_van")
    
    print("Servidor RPC LA FILA atendiendo en el puerto 5000...")
    servidor.serve_forever() # Deja al servidor atendiendo llamadas[cite: 5]