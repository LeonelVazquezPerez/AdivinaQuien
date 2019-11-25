#!/usr/bin/env python3

import socket
import time
global matriz
matriz = []


def actualizaMatriz(str):
    lista = list(str)
    print("lista:", lista)
    k = 0
    if dificultad == "1":
        for i in range(3):
            for j in range(3):
                matriz[i][j] = lista[k]
                k += 1
    else:
        for i in range(5):
            for j in range(5):
                matriz[i][j] = lista[k]
                k += 1


def dibujarGato():
    if dificultad == "1":
        for i in range(3):
            for j in range(3):
                print(" ",matriz[i][j], end="")
            print()
    else:
        for i in range(5):
            for j in range(5):
                print(" ",matriz[i][j], end="")
            print()


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234  # The port used by the server
buffer_size = 1024

print("**********************************************************************")
print("*                                                                    *")
print("*                          GATO DUMMY                                *")
print("*                                                                    *")
print("**********************************************************************")

print("Configuremos la partida.")
HOST= input("HOST al que te vas a conectar:")
PORT= int(input("PUERTO al que te vas a conectar:"))
dificultad = 0
jugador = 0


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Conectando con el servidor...")
    respuesta = TCPClientSocket.recv(buffer_size)
    print(respuesta.decode())
    respuesta = TCPClientSocket.recv(buffer_size)

    if respuesta.decode() == "jugador1":
        jugador = 1
        print("Eres el jugador 1, espere a que todos los jugadores se unan a la partida.")

        TCPClientSocket.sendall(b"esperando")
    else:
        jugador = int(respuesta.decode())
        print("El jugador 1 esta escogiendo la dificultad.")
        TCPClientSocket.sendall(b"esperando")










