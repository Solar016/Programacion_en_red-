#EJERCICIO 3 Servidor y cliente UDP simple (un cliente a la vez)
# --- SERVIDOR UDP ---
import socket

def servidor_udp():
    # SOCK_DGRAM indica que usaremos UDP[cite: 1]. En UDP no hay conexión persistente.
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Asignamos el puerto 5001. En UDP no se usa ni listen() ni accept()[cite: 1].
    server.bind(('', 5001))
    print("Servidor UDP escuchando en puerto 5001...")
    
    while True:
        # recvfrom recibe los datos y también la dirección exacta (IP y puerto) del cliente que los mandó[cite: 1].
        # En UDP, un datagrama es un mensaje completo[cite: 1].
        datos, direccion = server.recvfrom(1024)
        mensaje = datos.decode('utf-8')
        
        if mensaje == "ESTADO":
            # Para responder en UDP se usa sendto(), indicando los datos (en bytes) y la dirección destino[cite: 1].
            server.sendto("servidor activo".encode('utf-8'), direccion)

# --- CLIENTE UDP ---
def cliente_udp():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # settimeout(3) hace que si el recvfrom() tarda más de 3 segundos esperando, lance un error[cite: 1].
    cliente.settimeout(3) 
    
    try:
        # Enviamos el datagrama directamente a la IP y puerto sin conectarnos previamente.
        cliente.sendto("ESTADO".encode('utf-8'), ('localhost', 5001))
        
        # Esperamos la respuesta.
        datos, addr = cliente.recvfrom(1024)
        print(f"Respuesta UDP: {datos.decode('utf-8')}")
        
    except socket.timeout:
        # Si pasan los 3 segundos, atrapamos la excepción timeout[cite: 1].
        print("Error: El servidor tardó más de 3 segundos en responder.")
    finally:
        cliente.close()