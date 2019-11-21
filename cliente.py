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

    if respuesta.decode() == "configurar":
        jugador = 1

        fichita = input("Escribe cual sera tu fichita(un caracter): ")
        dificultad = input("Escoge la dificultad ( 1- Facil, 2- Dificil ):  ")
        TCPClientSocket.sendall(dificultad.encode())
    else:
        jugador = int(respuesta.decode())
        fichita = input("Player "+str(jugador)+"Escribe cual sera tu fichita(un caracter): ")
        print("El jugador 1 esta escogiendo la dificultad.")
        TCPClientSocket.sendall(b"esperando")

    bandera = True
    while bandera:
        data = TCPClientSocket.recv(buffer_size)
        paquete = data.decode().split("|")
        print("Paquete Recibido: ", paquete)

        if paquete[0] == "SIGUE":
            actualizaMatriz(paquete[1])
            dibujarGato()
            data = input("Selecciona la coordenada x,y para poner tu fichita "+fichita+":")
            coordenadas = data+","+fichita
            print("Enviando: ", coordenadas)
            TCPClientSocket.sendall(coordenadas.encode())
        elif paquete[0] == "INICIA":
            dificultad = paquete[1]
            if dificultad == "1":
                disponibles = 9
                for i in range(3):
                    matriz.append([])
                    for j in range(3):
                        matriz[i].append("-")
            else:
                disponibles = 25
                for i in range(5):
                    matriz.append([])
                    for j in range(5):
                        matriz[i].append("-")

            TCPClientSocket.sendall(b"Pido-Turno")
        elif paquete[0] == "OCUPADO":
            print("Es turno de otro jugador")
            time.sleep(1)
            TCPClientSocket.sendall(b"Pido-Turno")
        elif paquete[0] == "GANADOR":
            actualizaMatriz(paquete[1])
            dibujarGato()
            print(" Gano el jugador: " + paquete[2])
            bandera = False








