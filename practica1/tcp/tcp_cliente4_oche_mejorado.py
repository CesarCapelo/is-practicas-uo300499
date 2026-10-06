#!/usr/bin/env python3

import socket
import sys

IP_POR_DEFECTO = "localhost"
PUERTO_POR_DEFECTO = 9999


def recibe_mensaje(sock):
    """Lee del socket byte a byte hasta recibir el terminador \\r\\n.
    Retorna la línea completa (con el terminador) o b"" si se cierra
    la conexión"""
    buffer = []
    while buffer[-2:] != [b"\r", b"\n"]:
        byte = sock.recv(1)
        if byte == b"":
            break
        buffer.append(byte)
    return b"".join(buffer)


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

    lineas = ["UNO", "DOS", "TRES"]

    for linea in lineas:
        s.sendall(bytes(linea + "\r\n", "utf8"))

    for i in range(len(lineas)):
        respuesta = recibe_mensaje(s)
        respuesta = str(respuesta, "utf8")
        print(repr(respuesta))

    s.close()


if __name__ == "__main__":
    main()
