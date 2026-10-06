#!/usr/bin/env python3

import socket
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
        longitud = recibe_longitud(s)
        respuesta = str(recvall(s, longitud), "utf8")
        print(repr(respuesta))

    s.close()


if __name__ == "__main__":
    main()
