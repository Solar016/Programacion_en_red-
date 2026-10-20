import socket
IP_SERVIDOR = "localhost" 
PUERTO = 5050
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVIDOR, PUERTO))
print ("Conectado al servidor eco. Escriba mesanjes vacio para salir ")

while True:
    mensaje = input("usted dice: ")
    if mensaje == "":
        break
    cliente.sendall(mensaje.encode('utf-8'))
    eco =  cliente.recv(1024).decode('utf-8')
    print("servidor responde:", eco)

cliente.close()
print ("conexion cerrada")