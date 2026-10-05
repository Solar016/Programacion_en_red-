import socket

def iniciar_atacante_udp():
    host_defensor = '10.95.69.59'
    puerto_defensor = 5060
    direccion_defensor = (host_defensor, puerto_defensor)

    # 1. Configuración del Cliente UDP (SOCK_DGRAM)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print("¡Base de lanzamiento UDP lista! Prepara tu ataque.")

    while True:
        ataque = input("\nIngresa tu ataque (ej. B4): ")
        
        # send = encode (enviamos el dato y especificamos a dónde va)
        cliente.sendto(ataque.encode('utf-8'), direccion_defensor)

        # receive = decode (esperamos la respuesta del servidor)
        datos_recibidos, servidor_addr = cliente.recvfrom(1024)
            
        respuesta = datos_recibidos.decode('utf-8')
        print(f"Reporte de daños: {respuesta}")

    cliente.close()

if __name__ == "__main__":
    iniciar_atacante_udp()