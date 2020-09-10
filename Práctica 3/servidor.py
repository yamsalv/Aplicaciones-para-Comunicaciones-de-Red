# FALTA AGREGAR EL TIEMPO DE PARTIDA Y CUANDO GANA

import threading
from random import randint
import socket
import time
import traceback
from sys import argv
from os import system
from threading import Thread


HOST = "localhost"
PORT = 65432
buffer_size = 1024
listaConexiones = []
dificultadElegida = False
estadoJuego = '0'
tableroTapado = ""
tablero = []
frontPrincipiante = []
frontAvanzado = []
dificultad = '2'
iniciarPartida = threading.Event()
numeroJugadores = int(argv[1])
esTurno = True
is_active = True
tamBuf = '2'

def actualizarTablero(Client_conn):
    global listaConexiones
    global tamBuf
    if estadoJuego == '0' or estadoJuego == 'A':
        for conn in listaConexiones:
            conn.sendall("{}-{}-{}-{}".format(tamBuf, tableroTapado, dificultad, estadoJuego).encode())
    elif estadoJuego == 'F' or estadoJuego == 'W':
        tableroFinal = convertirCadena(tablero)
        for conn in listaConexiones:
            conn.sendall("{}-{}-{}-{}".format(tamBuf, tableroTapado, dificultad, estadoJuego).encode())
        Client_conn.close()
        listaConexiones.clear()
    elif estadoJuego == '1':
        Client_conn.sendall("{}-{}-{}-{}".format(tamBuf, tableroTapado, dificultad, estadoJuego).encode())


def seleccionDificultad(Client_conn):
    global tablero
    global tableroTapado
    global dificultad
    global dificultadElegida
    global estadoJuego
    global frontPrincipiante
    global frontAvanzado
    global tamBuf
    Client_conn.sendall("{}-{}-{}-{}".format(tamBuf, tableroTapado, dificultad, estadoJuego).encode())
    data = recibir_datos(Client_conn, buffer_size)
    system('cls')
    if data[2].lower() == 'p' and data[3] == 'e':
        dificultad = '0'
        tamBuf = '0'
        frontPrincipiante = crearMatriz(9, 9)
        print("¡El jugador es miedoso!\n\n")
        tablero = crearMatriz(9, 9)
        tablero = ponerMinas(9, 9, tablero, 10)
        tablero = ponerNumeros(tablero, 9, 9)
        for l in tablero:
           print(*l)
        print("\n\nSe genero ese tablero")
        tablero2 = crearMatriz(9, 9)
        tableroTapado = convertirCadena(tablero2)
        dificultadElegida = True
        return
    elif data[2].lower() == 'a' and data[3] == 'e':
        dificultad = '1'
        tamBuf = '1'
        frontAvanzado = crearMatriz(16, 16)
        print("¡El jugador es valiente!\n\n")
        tablero = crearMatriz(16, 16)
        tablero = ponerMinas(16, 16, tablero, 40)
        tablero = ponerNumeros(tablero, 16, 16)
        for l in tablero:
           print(*l)
        print("\n\nSe genero ese tablero")
        tablero2 = crearMatriz(16, 16)
        tableroTapado = convertirCadena(tablero2)
        dificultadElegida = True
        return


def client_thread(Client_conn, turno):
    global estadoJuego
    global is_active
    global esTurno
    iniciarPartida.wait()
    while is_active:
        while esTurno:
            if not is_active:
                break
            with turno:
                esTurno = True
                juego(Client_conn)
    actualizarTablero(Client_conn)
    print("Se ha terminado el juego")


def recibir_datos(Client_conn, max_buffer_size):
    data = Client_conn.recv(max_buffer_size).decode()
    data = data.split('-')
    return data


# Funciones del juego
def crearMatriz(filas, columnas, caracter="."):
    tablero = []
    for i in range(0,filas):
        v = [caracter]*columnas
        tablero.append(v)
    return tablero


def convertirCadena(tablero):
    cadena = ""
    for l in tablero:
        for c in l:
            if type(c) == int:
                cadena += str(c)
            else:
                cadena += c
    return cadena


def ponerMinas(filas,columnas,tablero,numMinas):
    mi = 1
    while mi <= numMinas:
        fil = randint(0,filas - 1)
        col = randint(0,columnas - 1)
        if tablero[fil][col] == ".":
            tablero[fil][col] = "*"
            mi += 1
    return tablero


def ponerNumeros(tablero,filas,columnas):
    nueva = crearMatriz(filas,columnas)
    for i in range(0,filas):
        for j in range(0,columnas):
            n = 0
            if i > 0 and j > 0 and tablero[i - 1][j - 1] == "*":
                n += 1
            if j > 0 and tablero[i][j - 1] == "*":
                n += 1
            if i < filas - 1 and j > 0 and tablero[i + 1][j - 1] == "*":
                n += 1
            if i > 0 and tablero[i - 1][j] == "*":
                n += 1
            if i < filas - 1 and tablero[i + 1][j] == "*":
                n += 1
            if i > 0 and j < columnas - 1 and tablero[i - 1][j + 1] == "*":
                n += 1
            if j < columnas - 1 and tablero[i][j + 1] == "*":
                n += 1
            if i < filas - 1 and j < columnas - 1 and tablero[i + 1][j + 1] == "*":
                n += 1
            if tablero[i][j] == ".":
                nueva[i][j] = n
            else:
                nueva[i][j] = "*"
    tablero = nueva
    return tablero



def destaparCeldas(filas, columnas, fila, columna, tablero2, nuevo):
    global tablero
    global frontPrincipiante
    global frontAvanzado
    nuevo[fila][columna] = tablero2[fila][columna]
    if tablero2[fila][columna] == 0:
        if fila > 0:
            if tablero2[fila - 1][columna] == "." and nuevo[fila - 1][columna] != 0:
                destaparCeldas(filas, columnas, fila - 1, columna, tablero2, nuevo)
            else:
                nuevo[fila - 1][columna] = tablero2[fila - 1][columna]
        if fila < filas - 1:
            if tablero2[fila + 1][columna] == "." and nuevo[fila + 1][columna] != 0:
                destaparCeldas(filas, columnas, fila + 1, columna, tablero2, nuevo)
            else:
                nuevo[fila + 1][columna] = tablero2[fila + 1][columna]
        if columna > 0:
            if tablero2[fila][columna - 1] == "." and nuevo[fila][columna - 1] != 0:
                destaparCeldas(filas, columnas, fila, columna - 1, tablero2, nuevo)
            else:
                nuevo[fila][columna - 1] = tablero2[fila][columna - 1]
        if columna < columnas - 1:
            if tablero2[fila][columna + 1] == "." and nuevo[fila][columna + 1] != 0:
                destaparCeldas(filas, columnas, fila, columna + 1, tablero2, nuevo)
            else:
                nuevo[fila][columna + 1] = tablero2[fila][columna + 1]
    frontPrincipiante = nuevo
    frontAvanzado = nuevo
    tablero = tablero2


def analizarDatos(data, Client_conn):
    global tableroTapado
    global frontPrincipiante
    global frontAvanzado
    global tablero
    global estadoJuego
    if len(data[0]) > 0 and len(data[1]) > 0 and data[2] == 'p' and data[3] == "j":
        count = tableroTapado.count(".")
        if count == 10:
            print("Ganador")
            tableroTapado = convertirCadena(tablero)
            end = time.time()
            tiempos = str(end - start)
            campos = tiempos.split('.')
            tiempo = ""
            tiempo += campos[0] + "." + campos[1][:2] + " segundos"
            estadoJuego = 'W'
        else:
            fila = int(data[0])
            columna = int(data[1])
            if type(tablero[fila - 1][columna - 1]) == int:
                frontPrincipiante[fila - 1][columna - 1] = tablero[fila - 1][columna - 1]
                if tablero[fila - 1][columna - 1] == 0:
                    destaparCeldas(9, 9, fila - 1, columna - 1, tablero, frontPrincipiante)
                tableroTapado = convertirCadena(frontPrincipiante)
                estadoJuego = 'A'
                actualizarTablero(Client_conn)
                estadoJuego = '1'
            else:
                tableroTapado = convertirCadena(tablero)
                estadoJuego = 'F'
                end = time.time()
                tiempos = str(end - start)
                campos = tiempos.split('.')
                tiempo = ""
                tiempo += campos[0] + "." + campos[1][:2] + " segundos"
    elif len(data[0]) > 0 and len(data[1]) > 0 and data[2] == 'a' and data[3] == "j":
        count = tableroTapado.count(".")
        if count == 40:
            print("Ganador")
            tableroTapado = convertirCadena(tablero)
            estadoJuego = 'W'
            end = time.time()
            tiempos = str(end - start)
            campos = tiempos.split('.')
            tiempo = ""
            tiempo += campos[0] + "" + campos[1][:2] + " segundos"
        else:
            fila = int(data[0])
            columna = int(data[1])
            if type(tablero[fila - 1][columna - 1]) == int:
                frontAvanzado[fila - 1][columna - 1] = tablero[fila - 1][columna - 1]
                if tablero[fila - 1][columna - 1] == 0:
                    destaparCeldas(16, 16, fila - 1, columna - 1, tablero, frontAvanzado)
                tableroTapado = convertirCadena(frontAvanzado)
                estadoJuego = 'A'
                actualizarTablero(Client_conn)
                estadoJuego = '1'
            else:
                tableroTapado = convertirCadena(tablero)
                estadoJuego = 'F'
                end = time.time()
                tiempos = str(end - start)
                campos = tiempos.split('.')
                tiempo = ""
                tiempo += campos[0] + "." + campos[1][:2] + " segundos"
                Client_conn.sendall("{}-{}-{}-{}-{}-{}".format("", "", msgCoordenada, tableroTapado, tiempo, dificultad).encode())
                juegoActivo = False
                return False

def juego(Client_conn):
    global tiempo
    global estadoJuego
    global is_active
    global esTurno
    if estadoJuego == 'F' or estadoJuego == 'W':
        is_active = False
        return
    actualizarTablero(Client_conn)
    data = recibir_datos(Client_conn, buffer_size)
    analizarDatos(data, Client_conn)
    esTurno = False


def main():
    global dificultadElegida
    global listaConexiones
    global estadoJuego
    print("¡Se ha abierto un campo de batalla para " + argv[1] + " jugadores!")
    turno = threading.Lock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind((HOST, PORT))
        TCPServerSocket.listen(numeroJugadores)
        while True:
            Client_conn, Client_addr = TCPServerSocket.accept()
            ip, port = str(Client_addr[0]), str(Client_addr[1])
            print("Se ha conectado un jugador por el puerto: " + str(port))
            listaConexiones.append(Client_conn)
            if len(listaConexiones) == numeroJugadores:
                print("¡Se han conectado todos los jugadores!\nLa partida va a comenzar en:")
                for i in range(3, 0, -1):
                    print(i)
                    time.sleep(1)
                system('cls')
                if not dificultadElegida:
                    print("Esperando a que el jugador 1 elija la dificultad")
                    seleccionDificultad(listaConexiones[0])
                    actualizarTablero(listaConexiones[0])
                    estadoJuego = '1'
                    iniciarPartida.set()
                for i in range(len(listaConexiones)):
                    try:
                        Thread(target=client_thread, args=(listaConexiones[i], turno)).start()
                    except:
                        print("Hubo un error.")
                        traceback.print_exc()
            else:
                print("Esperando al resto de jugadores")


if __name__ == '__main__':
    main()
