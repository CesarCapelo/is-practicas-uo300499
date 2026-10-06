#!/usr/bin/env python3

import socket
import sys

BROADCAST_POR_DEFECTO = "255.255.255.255"
PUERTO = 12345
TIMEOUT = 1


def main():
    if len(sys.argv) > 1:
        broadcast = sys.argv[1]
    else:
        broadcast = BROADCAST_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Buscamos servidores enviando por broadcast a toda la subred
    print("Buscando servidores HOLA en", broadcast)
    s.sendto("BUSCANDO HOLA".encode("utf8"), (broadcast, PUERTO))

    # Recogemos respuestas hasta que expire el timeout
    s.settimeout(TIMEOUT)
    primer_servidor = None
    while True:
        try:
            datagrama, origen = s.recvfrom(1024)
        except socket.timeout:
            break
        if datagrama.decode("utf8") == "IMPLEMENTO HOLA":
            print("Ha respondido el servidor", origen[0])
            if primer_servidor is None:
                primer_servidor = origen[0]

    if primer_servidor is None:
        print("No ha respondido ningún servidor")
        return

    # Probamos el servicio con el primer servidor que respondio
    print("Usando el servidor", primer_servidor)
    s.settimeout(None)
    s.sendto("HOLA".encode("utf8"), (primer_servidor, PUERTO))
    datagrama, origen = s.recvfrom(1024)
    print("Respuesta:", datagrama.decode("utf8"))

    s.close()


if __name__ == "__main__":
    main()
