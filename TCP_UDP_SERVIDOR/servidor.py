import socket
import threading

# Variable global compartida y su candado para evitar condiciones de carrera[cite: 1, 2]
contador_turnos = 0
cerrojo = threading.Lock() 

def atender_cliente_tcp(conexion, direccion):
    """Atiende a un cliente TCP en su propio hilo[cite: 1, 4]."""
    global contador_turnos
    
    with conexion:
        buffer = ""
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            
            buffer += datos.decode("utf-8") # TCP requiere decodificar[cite: 3, 7]
            
            # Procesamos cada línea separada por \n[cite: 3]
            while "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                
                if linea.startswith("TURNO>"): # Verifica el protocolo[cite: 6]
                    
                    # SECCIÓN CRÍTICA protegida por el candado[cite: 7]
                    with cerrojo:
                        contador_turnos += 1
                        mi_turno = contador_turnos
                    
                    # Responde con el número asignado[cite: 6]
                    respuesta = f"turno>{mi_turno}\n"
                    conexion.sendall(respuesta.encode("utf-8"))

def servidor_udp():
    """Atiende las consultas rápidas UDP en un hilo en segundo plano[cite: 5, 7]."""
    global contador_turnos
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("0.0.0.0", 5001)) # Puerto 5001[cite: 5]
    print("Servidor UDP escuchando en el puerto 5001")
    
    while True:
        datos, direccion = servidor.recvfrom(1024)
        mensaje = datos.decode("utf-8").strip()
        
        if mensaje == "CUANTOS": # Protocolo de consulta[cite: 6]
            respuesta = f"van>{contador_turnos}\n"
            servidor.sendto(respuesta.encode("utf-8"), direccion)

def main():
    # Arranca el servidor UDP en un hilo daemon[cite: 2, 7]
    hilo_udp = threading.Thread(target=servidor_udp, daemon=True)
    hilo_udp.start()

    # Configura el servidor TCP principal
    servidor_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Evita error de puerto usado[cite: 7]
    servidor_tcp.bind(("0.0.0.0", 5000)) # Puerto 5000[cite: 3]
    servidor_tcp.listen()
    print("Servidor TCP escuchando en el puerto 5000")

    while True:
        conexion, direccion = servidor_tcp.accept()
        
        # Lanza un hilo por cada cliente TCP que se conecta[cite: 1, 4]
        hilo_cliente = threading.Thread(
            target=atender_cliente_tcp, 
            args=(conexion, direccion), # Tupla obligatoria[cite: 7]
            daemon=True
        )
        hilo_cliente.start()

main()