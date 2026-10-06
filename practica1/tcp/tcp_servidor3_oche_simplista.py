#!/usr/bin/env python3

import socket
import sys
import time

PUERTO_POR_DEFECTO = 9999


def main():
    if len(sys.argv) > 1:
        puerto = int(sys.argv[1])
    else:
        puerto = PUERTO_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", puerto))
    s.listen(5)

    while True:
        print("Esperando un cliente")
        sd, origen = s.accept()
        print("Nuevo cliente conectado desde %s, %d" % origen)
        time.sleep(1)
        while True:
            # Primero recibir el mensaje del cliente
            mensaje = sd.recv(80)
            if mensaje == b"":
                print("El cliente ha cerrado la conexión")
                break
            mensaje = str(mensaje, "utf8")

            # Segundo, quitarle el "fin de línea" que son sus 2 últimos caracteres
            linea = mensaje[:-2]

            # Tercero, darle la vuelta
            linea = linea[::-1]

            # Finalmente, enviarle la respuesta con un fin de línea añadido
            sd.sendall(bytes(linea + "\r\n", "utf8"))
        sd.close()


if __name__ == "__main__":
    main()
