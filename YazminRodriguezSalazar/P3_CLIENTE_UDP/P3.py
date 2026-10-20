import socket
import time

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cliente.settimeout(3.0) 

esperas = [0, 1, 2, 4]

try:
    exito = False
    
    for intento, pausa in enumerate(esperas):
        if pausa > 0:
            print(f"\nEsperando {pausa} segundos antes de volver a intentar")
            time.sleep(pausa)
            
        print(f"Intento {intento + 1}: Enviando 'ESTADO' al puerto 5001...")
        cliente.sendto("ESTADO".encode(), ('localhost', 5001))
        
        try:
            respuesta, direccion = cliente.recvfrom(1024)
            print(f"Respuesta recibida del servidor: {respuesta.decode()}")
            exito = True
            break  
            
        except (socket.timeout, ConnectionResetError):
            print("Sin respuesta en este intento.")

    if not exito:
        print("\n ERROR, no se logro tener respuesta, el servidor no responde después de varios intentos.")

except Exception as e:
    print("\nOcurrió un error inesperado de red:", e)

finally:
    print("Cerrando el socket UDP...")
    cliente.close()