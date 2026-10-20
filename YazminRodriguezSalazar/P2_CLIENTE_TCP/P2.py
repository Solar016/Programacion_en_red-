import socket
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.settimeout(3.0) 

try:
    cliente.connect(('localhost', 5000))
    print("Conectado al servidor")
    
    mensajes = ["Hola\n", "Prueba \n", "Adios\n"]
    
    for mensaje in mensajes:
        print("Enviando:", mensaje.strip())
        cliente.send(mensaje.encode())
        
        respuesta = cliente.recv(1024).decode()
        print("Recibido:", respuesta.strip())
        
        time.sleep(1)

except socket.timeout:
    print("Error: El servidor tardó demasiado en responder.")
except socket.gaierror:
    print("Error: No se pudo resolver el nombre del servidor.")
except ConnectionRefusedError:
    print("Error: El servidor está apagado o rechazó la conexión.")
except Exception as e:
    print("Ocurrió un error inesperado:", e)

finally:
    print("Cerrando la conexión...")
    cliente.close()