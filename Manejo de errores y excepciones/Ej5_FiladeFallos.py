import socket
import threading

contador_turnos = 0
cerrojo = threading.Lock() 

def atender_cliente_tcp(conexion, direccion):
    global contador_turnos
    
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                
                # Atrapamos el error si el cliente manda basura que no es texto válido
                try:
                    buffer += datos.decode("utf-8")
                except UnicodeDecodeError:
                    print(f"[{direccion}] Error: El cliente envió bytes inválidos.")
                    break 
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    
                    # Solo damos turno si el mensaje empieza exactamente como dicta el protocolo
                    if linea.startswith("TURNO>"):
                        with cerrojo:
                            contador_turnos += 1
                            mi_turno = contador_turnos
                        
                        respuesta = f"turno>{mi_turno}\n"
                        conexion.sendall(respuesta.encode("utf-8"))
                    else:
                        print(f"[{direccion}] Error: Mensaje fuera de protocolo ('{linea}').")
                        
    # Atrapamos si el cliente cierra su terminal a la mitad o se le va el internet
    except ConnectionResetError:
        print(f"[{direccion}] Se desconectó abruptamente.")
    finally:
        print(f"[{direccion}] Hilo de atención terminado.")

def servidor_udp():
    """Atiende las consultas ligeras UDP en segundo plano."""
    global contador_turnos
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("0.0.0.0", 5001))
    print("Servidor UDP escuchando en el puerto 5001")
    
    while True:
        datos, direccion = servidor.recvfrom(1024)
        if datos.decode("utf-8").strip() == "CUANTOS":
            respuesta = f"van>{contador_turnos}\n"
            servidor.sendto(respuesta.encode("utf-8"), direccion)

def main():
    # Arranca el hilo para escuchar por UDP
    threading.Thread(target=servidor_udp, daemon=True).start()

    # Configura el servidor principal por TCP
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor_tcp.bind(("0.0.0.0", 5000))
    except OSError:
        print("Error: El puerto 5000 ya está ocupado.")
        return
        
    servidor_tcp.listen()
    print("Servidor TCP (Ejercicio 5) escuchando en puerto 5000")

    # El ciclo infinito que acepta a cada cliente nuevo y le asigna tu función
    while True:
        conexion, direccion = servidor_tcp.accept()
        threading.Thread(target=atender_cliente_tcp, args=(conexion, direccion), daemon=True).start()

# Esto es lo que hace que el programa arranque cuando le das 'Play'
if __name__ == "__main__":
    main()