import socket
import threading

def atender_cliente(conexion, direccion):
    """Atiende a un solo cliente y cuenta sus mensajes de forma independiente."""
    
        # tendrá su propio contador que empieza en cero[cite: 29].
    contador_mensajes = 0 
    
    # La red de seguridad (try/except) por si el cliente se desconecta feo[cite: 27]
    try:
        with conexion:
            buffer = ""
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break # El cliente se fue por las buenas
                
                buffer += datos.decode("utf-8")
                
                while "\n" in buffer:
                    linea, buffer = buffer.split("\n", 1)
                    
                    # Le sumamos 1 al contador porque llegó un mensaje nuevo[cite: 29]
                    contador_mensajes += 1 
                    
                    # se arma la respuesta con f-string como pide el profe[cite: 29]
                    respuesta = f"{contador_mensajes}>{linea}\n"
                    
                    # y se lo enviamos de regreso
                    conexion.sendall(respuesta.encode("utf-8"))
                    
    except ConnectionResetError:
        # Si el cliente cierra la terminal de golpe, no tumbamos el servidor[cite: 27]
        print(f"El cliente {direccion} se desconectó de forma abrupta.")
    finally:
        # Esto siempre se ejecuta para avisar que la conexión terminó[cite: 27]
        print(f"Conexión cerrada con: {direccion}")

def main():
    # Configuramos el servidor TCP en el puerto 5000[cite: 27]
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen()
    print("Servidor TCP con contador escuchando en el puerto 5000")

    while True:
        conexion, direccion = servidor.accept()
        # Creamos un hilo por cada cliente que llega
        hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion), daemon=True)
        hilo.start()

main()