import socket

PUERTO = 5050
servidor =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind(('0.0.0.0', PUERTO))
servidor.listen(1)
print("Servidor escuchando en el puerto", PUERTO)

conexion,direccion = servidor.accept()
print("cliente conectado desde", direccion)

while True:
    datos = conexion.recv(1024)
    if not datos:
        break
    mensaje = datos.decode('utf-8')
    print("Me llego:", mensaje)
    eco = "ECO> "+mensaje
    conexion.sendall(eco.encode('utf-8'))

    conexion.close()
    servidor.close()
    print ("conexion finalizada")
