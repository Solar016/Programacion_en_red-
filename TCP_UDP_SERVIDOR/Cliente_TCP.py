import socket

def main():
    # Se conecta al servidor TCP en el puerto 5000[cite: 4, 6]
    with socket.create_connection(("127.0.0.1", 5000)) as conexion:
        
        # Envia el mensaje pidiendo turno, no olvides el \n al final[cite: 6, 7]
        mensaje = "TURNO>Yazmin\n" 
        conexion.sendall(mensaje.encode("utf-8")) # Envía bytes codificados[cite: 7]
        
        # Espera la respuesta y la decodifica[cite: 4]
        respuesta_bytes = conexion.recv(1024)
        respuesta = respuesta_bytes.decode("utf-8").strip()
        
        print(f"Me conecté y el servidor respondió: {respuesta}")

main()