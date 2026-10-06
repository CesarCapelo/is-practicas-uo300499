#!/usr/bin/env python3

import socket
import sys

PUERTO_POR_DEFECTO = 9999


def recvall(sock, n):
    """Recibe exactamente n bytes del socket, salvo que el otro extremo
    cierre la conexión antes"""
    datos = b""
    while len(datos) < n:
        recibidos = sock.recv(n - len(datos))
        if recibidos == b"":
            break
        datos = datos + recibidos
    return datos


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
        continuar = True
        while continuar:
            datos = recvall(sd, 5)
            datos = datos.decode("ascii")
            if datos == "":
                print("Conexión cerrada de forma inesperada por el cliente")
                sd.close()
                continuar = False
            elif datos == "FINAL":
                print("Recibido mensaje de finalización")
                sd.close()
                continuar = False
            else:
                print("Recibido mensaje: %s" % datos)


if __name__ == "__main__":
    main()
