#!/usr/bin/env python3

import socket
import sys
import time

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
        time.sleep(1)
        while True:
            mensaje = recibe_mensaje(sd)
            if mensaje == b"":
                print("El cliente ha cerrado la conexión")
                break
            mensaje = str(mensaje, "utf8")
            linea = mensaje[:-2]
            linea = linea[::-1]
            sd.sendall(bytes(linea + "\r\n", "utf8"))
        sd.close()


if __name__ == "__main__":
    main()
