import socket
from os import system


HOST = "localhost"
PORT = 65432
respuestaDificultad = ''

def hacerTablero(cadena, n):
   tablero = []
   fila = []
   count = 0
   countCadena = 0
   while count < n:
      fila=[]
      for i in range(n):
         fila.append(cadena[countCadena])
         countCadena += 1
      tablero.append(fila)
      count += 1
   return tablero


def imprimirTablero(tablero):
   for l in tablero:
      print(*l)


def analizarDatos(data, TCPClientSocket):
    global respuestaDificultad
    tablero = []
    if data[1] == '':
        system('cls')
        print("Eres el encargado de elegir una dificultad:\n (P) Principiante (A) Avanzado")
        respuestaDificultad = input()
        TCPClientSocket.sendall("{}-{}-{}-{}".format("", "", respuestaDificultad, "e").encode())
        system('cls')
    elif len(data[1]) > 0 and len(data[2]) > 0 and data[3] == '0':
        system('cls')
        print("Ha iniciado la partida. \n¡Prepárate!\n\n")
        if data[2] == '0':
            tablero = hacerTablero(data[1], 9)
        elif data[2] == '1':
            tablero = hacerTablero(data[1], 16)
        imprimirTablero(tablero)
    elif len(data[1]) > 0 and len(data[2]) > 0 and data[3] == 'F':
        system('cls')
        if data[2] == '0':
            tablero = hacerTablero(data[1], 9)
        elif data[2] == '1':
            tablero = hacerTablero(data[1], 16)
        imprimirTablero(tablero)
        print("\n\nLa partida ha finalizado")
    elif len(data[1]) > 0 and len(data[2]) > 0 and data[3] == 'W':
        system('cls')
        if data[2] == '0':
            tablero = hacerTablero(data[1], 9)
        elif data[2] == '1':
            tablero = hacerTablero(data[1], 16)
        imprimirTablero(tablero)
        print("\n\n¡WINNER!")
    elif len(data[1]) > 0 and len(data[2]) > 0 and data[3] == 'A':
        system('cls')
        if data[2] == '0':
            tablero = hacerTablero(data[1], 9)
        elif data[2] == '1':
            tablero = hacerTablero(data[1], 16)
        imprimirTablero(tablero)
        print("\n\nUn jugador ha tirado. \nEspera tu turno")
    else:
        system('cls')
        if data[2] == '0':
            tablero = hacerTablero(data[1], 9)
            respuestaDificultad = 'p'
        elif data[2] == '1':
            tablero = hacerTablero(data[1], 16)
            respuestaDificultad = 'a'
        imprimirTablero(tablero)
        print("Es tu turno de tirar:\n\n")
        fila = input("Fila: ")
        columna = input("Columna: ")
        TCPClientSocket.sendall("{}-{}-{}-{}".format(fila, columna, respuestaDificultad, "j").encode())


def main():
    Juego = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((HOST, PORT))
        print("Se ha establecido la conexión\n")
        while Juego:
            data = TCPClientSocket.recv(1).decode()
            if data == '':
                print("Se cerró la conexión")
                Juego = False
                break
            if data[0] == '2':
                data = TCPClientSocket.recv(5).decode()
            elif data[0] == '0':
                data = TCPClientSocket.recv(86).decode()
            elif data[0] == '1':
                data = TCPClientSocket.recv(261).decode()
            data = data.split('-')
            analizarDatos(data, TCPClientSocket)


if __name__ == '__main__':
    main()
