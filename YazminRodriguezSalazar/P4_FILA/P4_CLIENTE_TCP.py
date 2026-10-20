import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect(('localhost', 5000))
    apodo = input("Ingresa tu apodo para pedir turno: ")
    
    mensaje = f"TURNO>{apodo}\n"
    cliente.send(mensaje.encode())
    
    respuesta = cliente.recv(1024).decode()
    print("Respuesta del servidor:", respuesta.strip())

except Exception as e:
    print("Error al conectar:", e)
finally:
    cliente.close()