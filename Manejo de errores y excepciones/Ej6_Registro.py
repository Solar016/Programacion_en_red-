import time

def registrar_error(direccion, mensaje_error):
    """Guarda el error en un archivo de texto con fecha y hora[cite: 30]."""
    
    fecha_hora = time.strftime("%Y-%m-%d %H:%M:%S") 
    
    # Armamos la línea de texto completa
    # Se verá así: 2026-10-06 10:32:15 ('127.0.0.1', 51020) conexión reiniciada
    linea_registro = f"{fecha_hora} {direccion} {mensaje_error}\n"
    
    # Abrimos el archivo en modo "a" (append) para que agregue al final sin borrar lo anterior
    with open("registro_errores.txt", "a") as archivo:
        archivo.write(linea_registro)