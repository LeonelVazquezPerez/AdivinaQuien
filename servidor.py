# !/usr/bin/env python3

import socket
import sys
import threading


def servirPorSiempre(socketTcp, listaconexiones, NoPlayers):
    num_threads = int(NoPlayers)
    barrier = threading.Barrier(num_threads)
    condition = threading.Condition()
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(name='Player-%s' % len(listaConexiones),
                                           target=recibir_datos,
                                           args=[barrier, client_conn, client_addr, condition])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(barrier, conn, addr,condicion):
    global activos
    try:
        cur_thread = threading.current_thread()
        player = cur_thread.name
        print("barrier : " + str(barrier.n_waiting) + "/ " + str(barrier.parties))
        if player == "Player-1":
            print(player + " esperando jugadores ")
            paquete = player + ", esperando a los demas jugadores"

        else:
            print(player + " uniendose a la partida del jugador 1")
            paquete = player + ", uniendose a la partida del jugador 1"
        conn.sendall(paquete.encode())
        player_id = barrier.wait()
        print(cur_thread.name + " en espera de partida", player_id)
        aux = int(player_id) + 1
        paquete = str(aux)
        conn.sendall(paquete.encode())
        print("Se envia el paquete : " + paquete)
        paquete = conn.recv(1024)

        paquete = "INICIA|"
        conn.sendall(paquete.encode())
        activos.append(player)
        global bolGano
        bolGano = False
        global playerGanador
        playerGanador = "nadie"
        while True:
            print("[" + player + "] : Entro")
            data = conn.recv(1024)
            print("[" + player + "] : Recibio ," + data.decode())
            if not semaforo.acquire(False):
                print("["+player+"] : El candado esta siendo usado")
                paquete = "OCUPADO|"
                print("En espera: " + str(activos))
                conn.sendall(paquete.encode())
            else:
                print("[" + player + "] : Obtuvo el candado")
                try:

                    if not bolGano:
                        if activos[0] == player:

                            print(data.decode())
                            paquete = "SIGUE|"+pistas.pop()
                            conn.sendall(paquete.encode())
                            print("[" + player + "] : esperando su tiro, fila =" + str(activos))
                            paquete = conn.recv(1024)
                            print("[" + player + "] :respuesta recibida: " + paquete.decode())
                            global personaje
                            print(paquete.decode() + " == " + personaje)
                            if paquete.decode() == personaje:
                                print("gano")
                                paquete = "GANADOR|" + str(player)

                                bolGano = True
                                playerGanador = player
                                activos.remove(player)
                            else:
                                activos.remove(player)
                                activos.append(player)
                                paquete = "OCUPADO|"
                            conn.sendall(paquete.encode())
                        else:
                            paquete = "OCUPADO|"
                            conn.sendall(paquete.encode())
                    else:
                        paquete = "GANADOR|"+str(playerGanador)
                        conn.sendall(paquete.encode())
                finally:
                    semaforo.release()
            if not data:
                print("Fin")
                break
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))
semaforo = threading.Semaphore(1)
activos = []

file = open("Datos.txt","r")
global personaje
personaje = file.readline().rstrip('\n')
print(personaje)
global pistas
pistas = []


for linea in file.readlines():
    print(linea)
    pistas.append(linea)

print("Personaje a adivinar: " + personaje)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    NoPlayers = input("Numero de jugadores para la partida: ")
    print("El servidor TCP está disponible y en espera de solicitudes")

    servirPorSiempre(TCPServerSocket, listaConexiones,NoPlayers)