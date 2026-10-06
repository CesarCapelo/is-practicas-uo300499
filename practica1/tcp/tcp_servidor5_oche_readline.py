#!/usr/bin/env python3

import socket
import sys
import time

PUERTO_POR_DEFECTO = 9999


def main():
    if len(sys.argv) > 1:
        puerto = int(sys.argv[1])
    else:
        puerto = PUERTO_POR_DEFECTO

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", puerto))
    s.listen(5)

    while True:
        print("Esperando un cliente", flush=True)
        sd, origen = s.accept()
        print("Nuevo cliente conectado desde %s, %d" % origen, flush=True)
        time.sleep(1)
        f = sd.makefile(encoding="utf8", newline="\r\n")
        while True:
            mensaje = f.readline()
            if mensaje == "":
                print("El cliente ha cerrado la conexión", flush=True)
                break
            linea = mensaje[:-2]
            linea = linea[::-1]
            sd.sendall(bytes(linea + "\r\n", "utf8"))
        f.close()
        sd.close()


if __name__ == "__main__":
    main()
