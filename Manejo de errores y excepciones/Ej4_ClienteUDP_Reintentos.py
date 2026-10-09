import socket
import time

def consultar_udp(servidor, mensaje, reintentos=3):
    """Envía la consulta UDP y reintenta si no hay respuesta."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        
        # Solo esperamos 2 segundos por intento
        cliente.settimeout(2) 
        
        # Ciclo que se repetirá máximo 3 veces
        for intento in range(1, reintentos + 1):
            try:
                # Enviamos "CUANTOS" al servidor
                cliente.sendto((mensaje + "\n").encode("utf-8"), servidor)
                
                # Si llega la respuesta, la decodificamos y salimos de la función
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
                
            except TimeoutError:
                espera = 2 ** (intento - 1) 
                print(f"Intento {intento} falló. Esperando {espera} segundos...")
                time.sleep(espera) # Hacemos la pausa
        
        # Si el ciclo de 3 intentos termina y nunca hubo respuesta, devolvemos None
        return None

def main():
    # Mandamos la consulta UDP usando la IP de pruebas
    resultado = consultar_udp(("127.0.0.1", 5001), "CUANTOS")
    
    # Verificamos qué devolvió la función para no imprimir "None"
    if resultado:
        print(f"El servidor de LA FILA dice: {resultado}")
    else:
        print("Error definitivo: El servidor no respondió después de 3 intentos.")

main()