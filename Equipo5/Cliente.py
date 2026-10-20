import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('10.251.175.59', 8080))
print("Conectado al servidor. Escribe tus mensajes.\n")

while True:
    # input() también es una función bloqueante, detiene el programa
    # hasta que des Enter en la consola.
    mensaje = input("Escribe un mensaje (o 'salir' para cerrar): ")

    if mensaje.lower() == 'salir':
        break

    # Enviar el mensaje escrito
    cliente.sendall(mensaje.encode('utf-8'))

cliente.close()
print("Desconectado.")