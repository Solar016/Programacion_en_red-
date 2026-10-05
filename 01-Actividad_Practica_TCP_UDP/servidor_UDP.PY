import socket

def iniciar_defensor_udp():
    host = '10.95.69.9'
    puerto = 5060

    barcos = ["A1", "A2", "A3", "C5", "D5", "G7"]
    
    # 1. Configuración del Servidor UDP (SOCK_DGRAM en lugar de SOCK_STREAM)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 2. Asignar el puerto (bind). ¡No hay listen ni accept en UDP!
    servidor.bind((host, puerto))
    
    print(f"Defensor UDP esperando ataques en el puerto {puerto}...")
    print(f"(Nuestra flota está en: {barcos})")
    
    while True:
        # receive = decode (espera recibir datos y la dirección de quien los envía)
        datos_recibidos, direccion_atacante = servidor.recvfrom(1024)
        
        ataque = datos_recibidos.decode('utf-8').strip().upper()
        print(f"\n¡Ataque recibido desde {direccion_atacante}! Coordenada: {ataque}")

        # Lógica del juego
        if ataque in barcos:
            respuesta = "TOCADO"
            barcos.remove(ataque)
        else:
            respuesta = "AGUA"
            
        print(f"Respuesta: {respuesta}")
        
        # send = encode (envía la respuesta directamente a la dirección del atacante)
        servidor.sendto(respuesta.encode('utf-8'), direccion_atacante)
        
        if len(barcos) == 0:
            print("\n¡Toda nuestra flota ha sido hundida!")
            break

    servidor.close()

if __name__ == "__main__":
    iniciar_defensor_udp()