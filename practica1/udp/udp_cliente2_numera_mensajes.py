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

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Enviando datagramas a {}:{} (escribe FIN para terminar)".format(ip, puerto))

    num_secuencia = 1
    while True:
        linea = input("> ")
        if linea == "FIN":
            break
        mensaje = "{}: {}".format(num_secuencia, linea)
        s.sendto(mensaje.encode("utf8"), (ip, puerto))
        num_secuencia += 1

    s.close()
    print("Cliente terminado")


if __name__ == "__main__":
    main()
