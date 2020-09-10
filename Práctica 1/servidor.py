from random import randint
import socket
import time


HOST = input("¿A qué dirección te deseas conectar?\n")
while True:
    PORT = input("¿A qué puerto te deseas conectar?\n")
    PORT = int(PORT)
    if PORT < 1024:
        print("Puerto inválido")
    else: break
buffer_size = 1024
msgDif = "Que dificultad deseas? (P) Principiante (A) Avanzado"
msgD1 = "Elegiste la dificultad Principiante"
msgD2 = "Elegiste la dificultad Avanzado"
msgCoordenada = "Indica la fila y la columna que deseas destapar"
conn, addr = None, None


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



def destaparCeldas(filas, columnas, fila, columna, tablero, nuevo):
    nuevo[fila][columna] = tablero[fila][columna]
    if tablero[fila][columna] == 0:
        if fila > 0:
            if tablero[fila - 1][columna] == "." and nuevo[fila - 1][columna] != 0:
                destaparCeldas(filas, columnas, fila - 1, columna, tablero, nuevo)
            else:
                nuevo[fila - 1][columna] = tablero[fila - 1][columna]
        if fila < filas - 1:
            if tablero[fila + 1][columna] == "." and nuevo[fila + 1][columna] != 0:
                destaparCeldas(filas, columnas, fila + 1, columna, tablero, nuevo)
            else:
                nuevo[fila + 1][columna] = tablero[fila + 1][columna]
        if columna > 0:
            if tablero[fila][columna - 1] == "." and nuevo[fila][columna - 1] != 0:
                destaparCeldas(filas, columnas, fila, columna - 1, tablero, nuevo)
            else:
                nuevo[fila][columna - 1] = tablero[fila][columna - 1]
        if columna < columnas - 1:
            if tablero[fila][columna + 1] == "." and nuevo[fila][columna + 1] != 0:
                destaparCeldas(filas, columnas, fila, columna + 1, tablero, nuevo)
            else:
                nuevo[fila][columna + 1] = tablero[fila][columna + 1]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()
    print("Esperando a que el jugador inicie una partida")
    Client_conn, Client_addr = TCPServerSocket.accept()
    print("¡Se ha abierto un campo de batalla!")
    start = time.time()
    with Client_conn:
        juego = True
        frontPrincipiante = crearMatriz(9, 9)
        frontAvanzado = crearMatriz(16, 16)
        Client_conn.sendall("{}-{}-{}-{}-{}".format(msgDif, "", "", "", "").encode())
        while juego:
            data = Client_conn.recv(buffer_size).decode()
            data = data.split('-')
            if data[2].lower() == 'p' and data[3] == 'e':
                print("¡El jugador es miedoso!")
                tablero = crearMatriz(9, 9)
                tablero = ponerMinas(9, 9, tablero, 10)
                tablero = ponerNumeros(tablero, 9, 9)
                print(tablero)
                print("Se genero ese tablero")
                print()
                print()
                tablero2 = crearMatriz(9, 9)
                tableroTapado = convertirCadena(tablero2)
                Client_conn.sendall("{}-{}-{}-{}-{}".format("", msgD1, msgCoordenada, tableroTapado, "").encode())
            elif data[2].lower() == 'a' and data[3] == 'e':
                print("¡El jugador es valiente!")
                tablero = crearMatriz(16, 16)
                tablero = ponerMinas(16, 16, tablero, 40)
                tablero = ponerNumeros(tablero, 16, 16)
                print(tablero)
                print("Se genero ese tablero")
                print()
                print()
                tablero2 = crearMatriz(16, 16)
                tableroTapado = convertirCadena(tablero2)
                Client_conn.sendall("{}-{}-{}-{}-{}".format("", msgD2, msgCoordenada, tableroTapado, "").encode())
            elif len(data[0]) > 0 and len(data[1]) > 0 and data[2] == 'p' and data[3] == "j":
                count = tableroTapado.count(".")
                if count == 10:
                    print("Ganador")
                    tableroTapado = convertirCadena(tablero)
                    end = time.time()
                    tiempos = str(end - start)
                    campos = tiempos.split('.')
                    tiempo = ""
                    tiempo += campos[0] + "." + campos[1][:2] + " segundos"
                    Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", "", tableroTapado, tiempo).encode())
                    juego = False
                    break
                else:
                    fila = int(data[0])
                    columna = int(data[1])
                    if type(tablero[fila - 1][columna - 1]) == int:
                        frontPrincipiante[fila - 1][columna - 1] = tablero[fila - 1][columna - 1]
                        if tablero[fila - 1][columna - 1] == 0:
                            destaparCeldas(9, 9, fila - 1, columna - 1, tablero, frontPrincipiante)
                        tableroTapado = convertirCadena(frontPrincipiante)
                        Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", msgCoordenada, tableroTapado, "").encode())
                    else:
                        tableroTapado = convertirCadena(tablero)
                        end = time.time()
                        tiempos = str(end - start)
                        campos = tiempos.split('.')
                        tiempo = ""
                        tiempo += campos[0] + "." + campos[1][:2] + " segundos"
                        Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", msgCoordenada, tableroTapado, tiempo).encode())
                        juego = False
                        break
            elif len(data[0]) > 0 and len(data[1]) > 0 and data[2] == 'a' and data[3] == "j":
                count = tableroTapado.count(".")
                if count == 40:
                    print("Ganador")
                    tableroTapado = convertirCadena(tablero)
                    end = time.time()
                    tiempos = str(end - start)
                    campos = tiempos.split('.')
                    tiempo = ""
                    tiempo += campos[0] + "" + campos[1][:2] + " segundos"
                    Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", "", tableroTapado, tiempo).encode())
                    juego = False
                    break
                else:
                    fila = int(data[0])
                    columna = int(data[1])
                    if type(tablero[fila - 1][columna - 1]) == int:
                        frontAvanzado[fila - 1][columna - 1] = tablero[fila - 1][columna - 1]
                        if tablero[fila - 1][columna - 1] == 0:
                            destaparCeldas(16, 16, fila - 1, columna - 1, tablero, frontAvanzado)
                        tableroTapado = convertirCadena(frontAvanzado)
                        Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", msgCoordenada, tableroTapado, "").encode())
                    else:
                        tableroTapado = convertirCadena(tablero)
                        end = time.time()
                        tiempos = str(end - start)
                        campos = tiempos.split('.')
                        tiempo = ""
                        tiempo += campos[0] + "." + campos[1][:2] + " segundos"
                        Client_conn.sendall("{}-{}-{}-{}-{}".format("", "", msgCoordenada, tableroTapado, tiempo).encode())
                        juego = False
                        break
