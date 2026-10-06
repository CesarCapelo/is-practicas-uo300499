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
    f = s.makefile(encoding="utf8", newline="\r\n")

    lineas = ["UNO", "DOS", "TRES"]

    for linea in lineas:
        s.sendall(bytes(linea + "\r\n", "utf8"))

    for i in range(len(lineas)):
        respuesta = f.readline()
        print(repr(respuesta))

    f.close()
    s.close()


if __name__ == "__main__":
    main()
