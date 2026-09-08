import socket

def iniciar_atacante():
    host = '10.95.69.59' # IP del defensor (cambiar si están en distintas computadoras)
    puerto = 5050

    # 1. Configuración del Cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 2. Inicia la comunicación con connect
    cliente.connect((host, puerto))
    print("¡Conectado a la base del Defensor! Prepara tu ataque.")

    # 3. Ciclo de juego (Blocking)
    while True:
        # Ingresar petición de ataque
        ataque = input("\nIngresa tu ataque (ej. B4): ")
        
        # send = encode (envía el texto)
        cliente.send(ataque.encode('utf-8'))

        # receive = decode (espera la respuesta)
        datos_recibidos = cliente.recv(1024)
        if not datos_recibidos:
            break
            
        respuesta = datos_recibidos.decode('utf-8')
        print(f"Reporte de daños: {respuesta}")

    cliente.close()

if __name__ == "__main__":
    iniciar_atacante()