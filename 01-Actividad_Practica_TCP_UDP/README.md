# 01 - Actividad Práctica Batalla Naval TCP / UDP

## Resumen de la actividad
En esta práctica se desarrolló un modelo cliente-servidor en Python simulando el juego "Batalla Naval" mediante el uso de sockets. 

Se desarrollaron dos arquitecturas de comunicación:
1.  **Protocolo TCP:** Se estableció una conexión directa y persistente usando `SOCK_STREAM`. El servidor (defensor) espera pasivamente (`bind`, `listen`, `accept`) mientras que el cliente (atacante) inicia la conexión (`connect`).
2.  **Protocolo UDP:** Se adaptó el juego para el envío de datagramas (`SOCK_DGRAM`), eliminando la necesidad de una conexión persistente y utilizando los métodos `recvfrom` y `sendto`.

Ambas versiones respetan el uso de `encode` y `decode` para la transmisión de datos, y cuentan con un servidor automatizado que verifica las coordenadas atacadas contra una lista de barcos para responder "AGUA" o "TOCADO".