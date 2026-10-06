#!/usr/bin/env python3

import socket
import struct
import sys

IP_POR_DEFECTO = "localhost"
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
        ip = sys.argv[1]
    else:
        ip = IP_POR_DEFECTO

    if len(sys.argv) > 2:
        puerto = int(sys.argv[2])
    else:
        puerto = PUERTO_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))

    mensajes = ["UNO", "DOS", "TRES", "Canción con eñe"]

    for mensaje in mensajes:
        envia_mensaje(s, mensaje)

    for i in range(len(mensajes)):
        longitud = struct.unpack(">H", recvall(s, 2))[0]
        respuesta = str(recvall(s, longitud), "utf8")
        print(repr(respuesta))

    s.close()


if __name__ == "__main__":
    main()
