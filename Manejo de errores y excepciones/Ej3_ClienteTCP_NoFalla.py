import socket
 import sys 

def main():
    # se le pide la IP al usuario
    ip_servidor = input("Ingresa la IP del servidor (ej. 127.0.0.1): ")
    
    # se  protege el intento de conectarse
    try:
        # Intentamos conectar con un tiempo máximo de espera de 5 segundos
        with socket.create_connection((ip_servidor, 5000), timeout=5) as conexion:
            
            # 3. Red de seguridad interna: protege el intercambio de mensajes
            try:
                conexion.sendall("hola\n".encode("utf-8"))
                respuesta = conexion.recv(1024).decode("utf-8").strip()
                print(f"El servidor dice: {respuesta}")
                
            except ConnectionResetError:
                # El servidor se apagó justo cuando estábamos hablando
                print("Error: El servidor cortó la conexión inesperadamente.")
                sys.exit(1) 
                
    # 4. Capturamos todos los errores posibles al intentar conectar
    except socket.gaierror:
        # Se activa si el usuario escribió "patata" en lugar de una IP
        print("Error: La IP o el nombre del servidor no es válido.")
        sys.exit(1) 
        
    except ConnectionRefusedError:
        # Se activa si la IP está bien, pero no hay ningún servidor prendido
        print("Error: El servidor está apagado o rechazó la conexión.")
        sys.exit(1) 
        
    except TimeoutError:
        # Se activa si el servidor existe pero se quedó "congelado"
        print("Error: El servidor tardó demasiado en responder.")
        sys.exit(1) 

main()