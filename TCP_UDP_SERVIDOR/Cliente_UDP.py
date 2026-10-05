import socket

def main():
    # Socket UDP (SOCK_DGRAM)[cite: 5]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        
        # Timeout de 3 segundos por si el servidor no responde[cite: 5, 7]
        cliente.settimeout(3) 
        
        # Consulta el total de turnos[cite: 6]
        mensaje = "CUANTOS".encode("utf-8")
        cliente.sendto(mensaje, ("127.0.0.1", 5001)) # Puerto 5001[cite: 6]
        
        try:
            # Espera la respuesta (ej. "van>3\n")[cite: 6]
            datos, _ = cliente.recvfrom(1024) 
            respuesta = datos.decode("utf-8").strip()
            print(f"Pantalla de la fila: {respuesta}")
            
        except TimeoutError:
            print("El servidor tardó mucho en responder o el paquete se perdió.")

main()