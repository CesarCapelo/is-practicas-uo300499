#!/usr/bin/env python3

import socket
import struct
import sys

PUERTO_POR_DEFECTO = 9999


def recvall(sock, n):
    datos = b""
    while len(datos) < n:
        recibidos = sock.recv(n - len(datos))
        if recibidos == b"":
            break
        datos = datos + recibidos
    return datos


def envia_mensaje(sock, mensaje):
    datos = bytes(mensaje, "utf8")
    sock.sendall(struct.pack(">H", len(datos)) + datos)


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
        while True:
            # La longitud viene en 2 bytes en big endian
            cabecera = recvall(sd, 2)
            if len(cabecera) < 2:
                print("El cliente ha cerrado la conexión")
                break
            longitud = struct.unpack(">H", cabecera)[0]
            mensaje = str(recvall(sd, longitud), "utf8")
            envia_mensaje(sd, mensaje[::-1])
        sd.close()


if __name__ == "__main__":
    main()
