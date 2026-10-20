import socket

PUERTO = 8080
TAMANO_BUFFER = 1024

# se crea el socket TCP 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se asocia el socket a todas las interfaces locales y al puerto definido
servidor.bind(('', PUERTO))

# el socket en modo escucha una conexion 
servidor.listen(1)

# bloquea y espera hasta que un cliente se conecte
conexion_cliente, direccion_cliente = servidor.accept()

# recibe datos enviados por el cliente
datos_recibidos = conexion_cliente.recv(TAMANO_BUFFER)

print("Datos recibidos:", datos_recibidos)

# se cierra la conexion con el cliente y el socket del servidor
conexion_cliente.close()
servidor.close()