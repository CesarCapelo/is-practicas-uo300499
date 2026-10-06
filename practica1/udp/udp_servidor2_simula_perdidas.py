#!/usr/bin/env python3

import random
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

        # 50% de probabilidad de simular que el datagrama se ha perdido
        if random.randint(0, 1) == 0:
            print("Simulando paquete perdido")
            continue

        texto = datagrama.decode("utf8")
        print("Recibido desde {}:{} -> {}".format(origen[0], origen[1], texto))


if __name__ == "__main__":
    main()
