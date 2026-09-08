import socket

def iniciar_defensor():
    host = '10.95.69.9' 
    puerto = 5050      

    # Lista con las coordenadas donde están ubicados nuestros barcos
    barcos = ["A1", "A2", "A3", "C5", "D5", "G7"]
    
    # Configuración del Servidor
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(1)
    
    print(f"Defensor esperando en el puerto {puerto}...")
    print(f"(Nuestra flota está en secreto en: {barcos})")
    
    conexion, direccion = servidor.accept()
    print(f"\n¡El atacante se ha conectado desde {direccion}!")

    # Ciclo de juego
    while True:
        # receive = decode (espera la petición/ataque)
        datos_recibidos = conexion.recv(1024)
        if not datos_recibidos:
            break
            
        # Decodificamos, limpiamos espacios y convertimos a mayúsculas
        # para que " a1 " o "a1" se lean correctamente como "A1"
        ataque = datos_recibidos.decode('utf-8').strip().upper()
        print(f"\n¡Nos atacan en la coordenada: {ataque}!")

        # VERIFICACIÓN AUTOMÁTICA
        if ataque in barcos:
            respuesta = "TOCADO"
            barcos.remove(ataque) # Quitamos esa parte del barco porque ya fue destruida
        else:
            respuesta = "AGUA"
            
        print(f"Nuestra respuesta automática: {respuesta}")
        
        # send = encode (envía la respuesta AGUA o TOCADO al atacante)
        conexion.send(respuesta.encode('utf-8'))
        
        # Condición extra: Si la lista de barcos se queda vacía, perdimos
        if len(barcos) == 0:
            print("\n¡Toda nuestra flota ha sido hundida! Fin de la partida.")
            # Enviamos un último mensaje al cliente indicando victoria (opcional)
            # conexion.send("¡HUNDIDO Y VICTORIA!".encode('utf-8')) 
            break

    conexion.close()
    servidor.close()

if __name__ == "__main__":
    iniciar_defensor()