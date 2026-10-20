#EJERCICIO 1 Servidor TCP simple (un cliente a la vez)

import socket # Módulo necesario para las conexiones de red[cite: 1]

def servidor_tcp():
    # 1. Crear el socket TCP. 
    # AF_INET significa que usaremos direcciones IPv4.
    # SOCK_STREAM significa que usaremos el protocolo TCP.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Permitir reutilizar el puerto tras reiniciarlo[cite: 1].
    # SOL_SOCKET y SO_REUSEADDR le dicen al sistema operativo que libere el puerto de inmediato si cerramos el programa.
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 3. Vincular el socket a una dirección y puerto (bind)[cite: 1].
    # '' significa que escuchará en todas las interfaces de red de la máquina. El puerto es 5000.
    server.bind(('', 5000))
    
    # 4. Poner el servidor en modo "escucha" (listen)[cite: 1].
    server.listen()
    print("Servidor TCP escuchando en puerto 5000...")
    
    # 5. Aceptar una conexión entrante (accept)[cite: 1].
    # Esto detiene el programa hasta que un cliente se conecta. Devuelve la conexión (conn) y la IP/puerto del cliente (addr).
    conn, addr = server.accept()
    print(f"Conectado a {addr}")
    
    # Acumularemos los datos aquí (buffer) para el framing por salto de línea[cite: 1].
    buffer = "" 
    
    while True:
        # Recibir hasta 1024 bytes del cliente.
        datos = conn.recv(1024)
        
        # Si el recv() devuelve vacío (b''), significa que el cliente cerró la conexión[cite: 1].
        if not datos:
            break
            
        # Convertir los bytes recibidos a texto (UTF-8) y agregarlos al buffer[cite: 1].
        buffer += datos.decode('utf-8')
        
        # Framing: Mientras haya un salto de línea (\n) en el buffer, extraemos un mensaje completo[cite: 1].
        while '\n' in buffer:
            # Separamos el buffer en dos partes: el primer mensaje y el resto del buffer.
            mensaje, buffer = buffer.split('\n', 1)
            print(f"Recibido: {mensaje}")
            
            # Reenviar al cliente (Eco) el mismo mensaje con su salto de línea.
            respuesta = f"{mensaje}\n"
            # sendall exige bytes, por lo que usamos encode()[cite: 1].
            conn.sendall(respuesta.encode('utf-8'))
            
    # Cerrar la conexión limpia con el cliente.
    conn.close()