import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cliente.settimeout(3.0)

try:
    print("Preguntando al servidor cuantos turnos van...")
    cliente.sendto("CUANTOS".encode(), ('localhost', 5001))
    
    respuesta, direccion = cliente.recvfrom(1024)
    print("Respuesta del servidor:", respuesta.decode())

except socket.timeout:
    print("El servidor no respondió a tiempo.")
except Exception as e:
    print("Error:", e)
finally:
    cliente.close()