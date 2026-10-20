import socket

# se crea el socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se conecta al servidor en el puerto 8080
cliente.connect(('localhost', 8080))

# se envia un mensaje en formato bytes
cliente.send(b"hola servidor")

cliente.close()


