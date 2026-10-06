#!/usr/bin/env python3

import socket
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


def recibe_longitud(sock):
    """Lee byte a byte hasta el delimitador \\n y retorna la longitud
    como entero, o None si se cierra la conexión"""
    buffer = []
    while True:
        byte = sock.recv(1)
        if byte == b"":
            return None
        if byte == b"\n":
            break
        buffer.append(byte)
    return int(b"".join(buffer))


def envia_mensaje(sock, mensaje):
    longitud = "%d\n" % len(bytes(mensaje, "utf8"))
    sock.sendall(bytes(longitud + mensaje, "utf8"))


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
            longitud = recibe_longitud(sd)
            if longitud is None:
                print("El cliente ha cerrado la conexión")
                break
            mensaje = str(recvall(sd, longitud), "utf8")
            envia_mensaje(sd, mensaje[::-1])
        sd.close()


if __name__ == "__main__":
    main()
