import socket
import threading

def atender_cliente(conexion, direccion):
    print("Se conectó:", direccion)
    buffer = ""
    try:
        while True:
            datos = conexion.recv(1024).decode()
            if not datos:
                break
            
            buffer = buffer + datos
            
            if "\n" in buffer:
                partes = buffer.split("\n")
                mensaje = partes[0]
                buffer = partes[1] 
                
                print(f"Mensaje de {direccion}: {mensaje}")
                
                eco = "ECO: " + mensaje + "\n"
                conexion.send(eco.encode())
                
    except:
        print("Error con el cliente", direccion)
    finally:
        conexion.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('localhost', 5000))
servidor.listen(5)
print("Servidor encendido en el puerto 5000, en espera de conexiones...")

while True:
    conexion, direccion = servidor.accept()
    hilo = threading.Thread(target=atender_cliente, args=(conexion, direccion))
    hilo.start()