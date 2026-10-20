#EJERCICIO 4 Servidor TCP multicliente (un hilo por cliente)
import socket
import threading

def atender_cliente(conn, addr):
    print(f"Hilo iniciado para {addr}")
    buffer = ""
    
    # En el Ejercicio 4, asumimos que nada falla (no hay try/except).
    while True:
        datos = conn.recv(1024)
        if not datos:
            break
            
        buffer += datos.decode('utf-8')
        while '\n' in buffer:
            mensaje, buffer = buffer.split('\n', 1)
            conn.sendall(f"{mensaje}\n".encode('utf-8'))
            
    # Cierre normal
    print(f"Cerrando conexión con {addr}")
    conn.close()

def servidor_tcp_hilos():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 5000))
    server.listen()
    print("Servidor TCP Multicliente (Ej 4) en puerto 5000...")
    
    while True:
        # El hilo principal solo acepta
        conn, addr = server.accept()
        # Se lanza un hilo por cliente
        hilo = threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True)
        hilo.start()

if __name__ == "__main__":
    servidor_tcp_hilos()