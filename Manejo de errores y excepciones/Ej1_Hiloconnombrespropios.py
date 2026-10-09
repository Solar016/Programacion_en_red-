import threading
import time

def saludar(nombre, repeticiones):
    """Imprime saludos según la cantidad indicada."""
    for i in range(repeticiones):
        print(f"{nombre} dice: hola {i + 1}")
        # Pausa de 1 segundo para ver cómo se mezclan los mensajes
        time.sleep(1)

def main():
    # La lista de tuplas que pide el ejercicio
    datos_hilos = [("Ana", 3), ("Beto", 5), ("Cora", 2)] 
    
    # Aquí se guardaran los hilos creados para poder esperarlos después
    lista_de_hilos = []


    for nombre, repeticiones in datos_hilos:
        #  se crea el hilo y le pasamos sus argumentos
        hilo = threading.Thread(target=saludar, args=(nombre, repeticiones))
        hilo.start() 
        lista_de_hilos.append(hilo) # Lo guardamos en nuestra lista

    for hilo in lista_de_hilos:
        hilo.join() # Esto detiene al programa principal hasta que este hilo acabe

    print("Fin del programa")

main()