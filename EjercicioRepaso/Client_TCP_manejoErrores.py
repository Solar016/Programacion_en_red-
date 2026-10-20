#EJERCICIO 2 Cliente TCP simple (un cliente a la vez)
import socket

def cliente_tcp():
    try:
        # create_connection es una forma rápida de conectar pasando una tupla (IP, puerto)[cite: 1].
        # 'localhost' es nuestra propia máquina.
        cliente = socket.create_connection(('localhost', 5000))
        
        # Los mensajes que vamos a enviar. Cada uno termina en \n como dicta la regla del protocolo[cite: 1].
        mensajes = ["hola\n", "redes\n", "adios\n"]
        
        for msg in mensajes:
            # encode() convierte el texto a bytes para poder enviarlo por la red[cite: 1].
            cliente.sendall(msg.encode('utf-8'))
            
            # Recibimos la respuesta y le hacemos decode() para volver a convertir de bytes a texto[cite: 1].
            respuesta = cliente.recv(1024).decode('utf-8')
            # strip() quita el salto de línea al imprimir para que no se vea doble espacio.
            print(f"Eco del servidor: {respuesta.strip()}")
            
    # Ejercicio 5: Informar con un mensaje claro si el servidor está apagado (ConnectionRefusedError)[cite: 1].
    except ConnectionRefusedError:
        print("Error: El servidor está apagado o no acepta conexiones.")
    # Ejercicio 5: Informar si la IP no se puede resolver (gaierror)[cite: 1].
    except socket.gaierror:
        print("Error: No se pudo resolver la dirección IP.")
    # Manejar cualquier otra caída repentina en medio de la conversación[cite: 1].
    except ConnectionResetError:
        print("Error: El servidor se cayó a mitad de la conversación.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        # El bloque finally siempre se ejecuta, asegurando que cerramos el socket pase lo que pase[cite: 1].
        cliente.close()