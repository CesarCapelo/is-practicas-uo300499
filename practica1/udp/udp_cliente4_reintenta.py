#!/usr/bin/env python3

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
    print("Enviando datagramas a {}:{} (escribe FIN para terminar)".format(ip, puerto))

    num_secuencia = 1
    while True:
        linea = input("> ")
        if linea == "FIN":
            break

        mensaje = "{}: {}".format(num_secuencia, linea)
        timeout = TIMEOUT_INICIAL
        confirmado = False

        # Reenviamos el mismo datagrama duplicando el timeout hasta recibir
        # el OK o hasta que el timeout supere el maximo
        while not confirmado and timeout <= TIMEOUT_MAXIMO:
            s.sendto(mensaje.encode("utf8"), (ip, puerto))
            s.settimeout(timeout)
            try:
                datagrama, origen = s.recvfrom(1024)
                datagrama = datagrama.decode("utf8")
                if datagrama == "OK":
                    print("Recibida confirmación")
                    confirmado = True
                else:
                    print("Recibido datagrama no esperado")
            except socket.timeout:
                print("No llega la confirmación (timeout {}s). Reintentando".format(timeout))
                timeout = timeout * 2
            except:
                raise

        if not confirmado:
            print("Puede que el servidor esté caído. Inténtelo más tarde")
            break

        num_secuencia += 1

    s.close()
    print("Cliente terminado")


if __name__ == "__main__":
    main()
