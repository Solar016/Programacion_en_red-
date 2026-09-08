print("=== ejercicio 1 =====")
mi_ip = "10.50.15.2"
mi_puerto = 5000
print(f"Resultado: {mi_ip}:{mi_puerto}\n")


print("=== ejercicio 2 ====")
def es_puerto_valido(puerto):
    return 0 <= puerto <= 65535
print(f"El puerto {mi_puerto} es válido: {es_puerto_valido(mi_puerto)}")



print("=== ejercicio 3 ====")
mensaje = "ana>luis:nos vemos a las 3"
campos = mensaje.replace(">", ":").split(":")

emi = campos[0]
recep = campos[1]
texto = campos[2]

print("La persona que envía el mensaje:", emi)
print("La persona que recibe el mensaje:", recep)
print("Texto:", texto)


print("=== ejercicio 4 ====")
# Aplicamos encode y decode a la variable 'texto' del ejercicio 3
texto_codificado = texto.encode('utf-8')
print("Codificado a bytes:", texto_codificado)

texto_decodificado = texto_codificado.decode('utf-8')
print("Decodificado a string:", texto_decodificado)