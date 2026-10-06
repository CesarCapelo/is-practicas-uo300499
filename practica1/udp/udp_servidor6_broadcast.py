#!/usr/bin/env python3

import socket

PUERTO = 12345


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", PUERTO))
    print("Servidor HOLA escuchando en el puerto", PUERTO, flush=True)

    while True:
        datagrama, origen = s.recvfrom(1024)
        texto = datagrama.decode("utf8")
        print("Recibido desde {}:{} -> {}".format(origen[0], origen[1], texto), flush=True)

        if texto == "BUSCANDO HOLA":
            s.sendto("IMPLEMENTO HOLA".encode("utf8"), origen)
        elif texto == "HOLA":
            respuesta = "HOLA: {}".format(origen[0])
            s.sendto(respuesta.encode("utf8"), origen)


if __name__ == "__main__":
    main()
