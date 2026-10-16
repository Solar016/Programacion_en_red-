import socket
import threading

# Contador compartido en memoria para llevar los turnos.
turnos_asignados = 0

# Lock, es el que protege variables compartidas. Evita que dos hilos sumen "1" al mismo tiempo y entreguen el mismo turno
lock = threading.Lock()

# Hilo para clientes TCP
def atender_cliente_tcp(conn, addr):
    global turnos_asignados # Le decimos que use la variable global.
    buffer = ""
    try:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            buffer += datos.decode('utf-8')
            while '\n' in buffer:
                mensaje, buffer = buffer.split('\n', 1)
                
                # Si el cliente manda el comando TURNO>apodo
                if mensaje.startswith("TURNO>"):
                    apodo = mensaje.split(">")[1]
                    
                    # Solo un hilo a la vez puede entrar aquí
                    with lock:
                        turnos_asignados += 1 # Aumentamos turno
                        turno_actual = turnos_asignados # Guardamos qué turno nos tocó
                    
                    # Respondemos turno>N\n
                    respuesta = f"turno>{turno_actual}\n"
                    conn.sendall(respuesta.encode('utf-8'))
                    print(f"Asignado turno {turno_actual} a {apodo}")
    except ConnectionResetError:
        pass
    finally:
        conn.close()

# Hilo dedicado únicamente al servidor UDP
def ciclo_udp():
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind(('', 5001)) # UDP escucha en el puerto 5001.
    
    while True:
        datos, addr = server_udp.recvfrom(1024)
        mensaje = datos.decode('utf-8')
        
        # Ante el datagrama CUANTOS respondemos el total.
        if mensaje == "CUANTOS":
            # Leemos de forma segura el contador
            with lock:
                total = turnos_asignados
                
            # Respondemos van>N\n
            respuesta = f"van>{total}\n"
            server_udp.sendto(respuesta.encode('utf-8'), addr)

def iniciar_servidor():
    # Lanzar un hilo independiente que correrá el ciclo UDP de por vida.
    hilo_udp = threading.Thread(target=ciclo_udp, daemon=True)
    hilo_udp.start()
    
    # El hilo principal se encargará de ser el servidor TCP
    server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_tcp.bind(('', 5000)) # TCP escucha en el puerto 5000
    server_tcp.listen()
    
    while True:
        conn, addr = server_tcp.accept()
        # Por cada cliente TCP, se lanza un hilo independiente
        hilo_tcp = threading.Thread(target=atender_cliente_tcp, args=(conn, addr), daemon=True)
        hilo_tcp.start()