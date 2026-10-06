#!/usr/bin/env python3

import socket
import sys

PUERTO_POR_DEFECTO = 9999


def main():
    if len(sys.argv) > 1:
        puerto = int(sys.argv[1])
    else:
        puerto = PUERTO_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", puerto))
    print("Servidor UDP escuchando en el puerto", puerto)

    while True:
        datagrama, origen = s.recvfrom(1024)
        texto = datagrama.decode("utf8")
        print("Recibido desde {}:{} -> {}".format(origen[0], origen[1], texto))


if __name__ == "__main__":
    main()
