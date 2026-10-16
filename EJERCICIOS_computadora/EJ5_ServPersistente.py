import socket
import threading

def atender_cliente(conn, addr):
    print(f"Hilo iniciado para {addr}")
    buffer = ""
    
    try:
        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            
            buffer += datos.decode('utf-8')
            while '\n' in buffer:
                mensaje, buffer = buffer.split('\n', 1)
                conn.sendall(f"{mensaje}\n".encode('utf-8'))
                
    # Atrapa la desconexión abrupta
    except ConnectionResetError:
        print(f"El cliente {addr} se desconectó abruptamente.")
        
    # finally asegura que el socket se cierre siempre 
    finally:
        print(f"Cerrando y limpiando conexión con {addr}")
        conn.close()

def servidor_tcp_persistente():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 5000))
    server.listen()
    print("Servidor TCP Persistente (Ej 5b) en puerto 5000...")
    
    while True:
        conn, addr = server.accept()
        hilo = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
        hilo.start()

if __name__ == "__main__":
    servidor_tcp_persistente()