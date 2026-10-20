import socket
import threading

contador_turnos = 0
lock = threading.Lock()

def atender_cliente_tcp(conexion, direccion):
    global contador_turnos
    try:
        buffer = ""
        while True:
            datos = conexion.recv(1024).decode()
            if not datos:
                break 
            
            buffer += datos
            
            if "\n" in buffer:
                partes = buffer.split("\n", 1)
                mensaje = partes[0]
                buffer = partes[1]
                
                if mensaje.startswith("TURNO>"):
                    apodo = mensaje.split("TURNO>")[1]
                    
                    with lock:
                        contador_turnos += 1
                        turno_asignado = contador_turnos
                        
                    print(f"Asignado turno {turno_asignado} a {apodo}")
                    respuesta = f"turno>{turno_asignado}\n"
                    conexion.send(respuesta.encode())
                    
    except Exception as e:
        print(f"Error TCP con el cliente {direccion}: {e}")
    finally:
        conexion.close()

def ciclo_tcp():
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.bind(('localhost', 5000))
    servidor_tcp.listen(5)
    print("Servidor TCP escuchando en el puerto 5000...")
    
    while True:
        try:
            conexion, direccion = servidor_tcp.accept()
            hilo_cliente = threading.Thread(target=atender_cliente_tcp, args=(conexion, direccion))
            hilo_cliente.start()
        except Exception as e:
            print("Error al aceptar conexión TCP:", e)

def ciclo_udp():
    global contador_turnos
    servidor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor_udp.bind(('localhost', 5001))
    print("Servidor UDP  escuchando en el puerto 5001...")
    
    while True:
        try:
            datos, direccion = servidor_udp.recvfrom(1024)
            mensaje = datos.decode().strip()
            
            if mensaje == "CUANTOS":
                with lock:
                    total = contador_turnos
                    
                respuesta = f"van>{total}"
                servidor_udp.sendto(respuesta.encode(), direccion)
                print(f"Consulta UDP desde {direccion}: van {total}")
                
        except Exception as e:
            print("Error en el servidor UDP:", e)

if __name__ == "__main__":
    hilo_udp = threading.Thread(target=ciclo_udp)
    hilo_udp.start()
    
    ciclo_tcp()