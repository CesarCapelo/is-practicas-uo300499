#!/usr/bin/env python3

import random
import socket
import sys

IP_POR_DEFECTO = "localhost"
PUERTO_POR_DEFECTO = 9999
TIMEOUT_INICIAL = 0.1
TIMEOUT_MAXIMO = 2


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
    # Con connect() solo se aceptan datagramas que vengan del servidor
    s.connect((ip, puerto))
    print("Enviando datagramas a {}:{} (escribe FIN para terminar)".format(ip, puerto))

    while True:
        linea = input("> ")
        if linea == "FIN":
            break

        # Identificador aleatorio, el mismo para todos los reenvios
        identificador = str(random.randint(0, 2**32))
        mensaje = "{}: {}".format(identificador, linea)
        timeout = TIMEOUT_INICIAL
        confirmado = False

        while not confirmado and timeout <= TIMEOUT_MAXIMO:
            s.send(mensaje.encode("utf8"))
            s.settimeout(timeout)
            try:
                datagrama = s.recv(1024)
                datagrama = datagrama.decode("utf8")
                if datagrama == "OK {}".format(identificador):
                    print("Recibida confirmación")
                    confirmado = True
                else:
                    print("Recibido datagrama no esperado")
            except (socket.timeout, ConnectionRefusedError):
                print("No llega la confirmación (timeout {}s). Reintentando".format(timeout))
                timeout = timeout * 2
            except:
                raise

        if not confirmado:
            print("Puede que el servidor esté caído. Inténtelo más tarde")
            break

    s.close()
    print("Cliente terminado")


if __name__ == "__main__":
    main()
