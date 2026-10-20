import xmlrpc.client

def iniciar_cliente():
    # El proxy es el stub que empaca y envía los datos de forma invisible[cite: 5]
    servidor = xmlrpc.client.ServerProxy("http://10.187.80.59.:5000")
    
    # El cliente pide el apodo por teclado[cite: 5]
    apodo = input("Ingresa tu apodo: ")
    
    try:
        # Llama las funciones como si fueran locales y muestra los resultados[cite: 5]
        turno = servidor.tomar_turno(apodo)
        print(f"Éxito. Tu turno asignado es: {turno}")
        
        total = servidor.cuantos_van()
        print(f"Total de turnos en la fila hasta ahora: {total}")
        
    except Exception as e:
        print(f"Ocurrió un error al contactar al servidor: {e}")

if __name__ == "__main__":
    iniciar_cliente()