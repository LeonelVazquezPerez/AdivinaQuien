#!/usr/bin/env python3
import os
import socket
import time
from Reconocimiento import recAudio
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server
buffer_size = 1024
jugador = 0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conectando con el servidor...")
    respuesta = TCPClientSocket.recv(buffer_size)
    print(respuesta.decode())
    jugador = TCPClientSocket.recv(buffer_size)
    print(jugador)
    TCPClientSocket.sendall(b"listo")
    bandera = True
    while bandera:
        data = TCPClientSocket.recv(buffer_size)
        paquete = data.decode().split("|")

        if paquete[0] == "INICIA":
            pistas = paquete[1].split(",")
            print("Inicia el juego. Estas son las pistas: ")
            for pista in pistas:
                print(pista)
            TCPClientSocket.sendall(b"Pido-Turno")
        elif paquete[0] == "SIGUE":
            time.sleep(1)
            print("Siguiente Pista: ")
            print(paquete[1])
            print("Dime quien crees que sea")
            respuesta = recAudio()
            print("Enviando tamanio del audio")
            with open("microaudio.wav", "rb") as f:
                content = f.read()
                TCPClientSocket.sendall(str(len(content)).encode())

            data = TCPClientSocket.recv(buffer_size)
            print("Recibio paquete de salida")
            if data.decode() == "OK":
                with open("microaudio.wav", "rb") as f:
                    print("Enviando archivo...")
                    TCPClientSocket.sendfile(f, 0)
                    print("Termino de enviar")
                    #TCPClientSocket.sendall(b"termino")
        elif paquete[0] == "OCUPADO":
            time.sleep(1)
            TCPClientSocket.sendall(b"Pido-Turno")
        elif paquete[0] == "GANADOR":
            print("Gano el jugador : " + paquete[1])
            bandera = False

