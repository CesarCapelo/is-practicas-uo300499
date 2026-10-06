#!/usr/bin/env python3

import socket
import sys

IP_POR_DEFECTO = "localhost"
PUERTO_POR_DEFECTO = 9999


def main():
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    else:
        ip = IP_POR_DEFECTO

    if len(sys.argv) > 2:
        puerto = int(sys.argv[2])
    else:
        puerto = PUERTO_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))

    lineas = ["UNO", "DOS", "TRES"]

    # Primero se envian los tres mensajes seguidos
    for linea in lineas:
        s.sendall(bytes(linea + "\r\n", "utf8"))

    # Despues se leen las tres respuestas
    for i in range(len(lineas)):
        respuesta = s.recv(80)
        respuesta = str(respuesta, "utf8")
        print(repr(respuesta))

    s.close()


if __name__ == "__main__":
    main()
