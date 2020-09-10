import socket


HOST = input("¿A qué dirección te deseas conectar?\n")
while True:
    PORT = input("¿A qué puerto te deseas conectar?\n")
    PORT = int(PORT)
    if PORT < 1024:
        print("Puerto inválido")
    else: break
buffer_size = 1024
juego = True


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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Se ha establecido la conexión\n")
    while juego:
        data = TCPClientSocket.recv(buffer_size).decode()
        data = data.split('-')
        if len(data[0]) > 0 and len(data[1]) == 0 and len(data[2]) == 0 and len(data[3]) == 0 and len(data[4]) == 0:
            print(data[0])
            respuestaDificultad = input()
            TCPClientSocket.sendall("{}-{}-{}-{}".format("", "", respuestaDificultad, "e").encode())
        elif len(data[0]) == 0 and len(data[1]) > 0 and len(data[2]) > 0 and len(data[3]) > 0 and len(data[4]) == 0:
            system('clear')
            print(data[1])
            print()
            print()
            if respuestaDificultad.lower() == 'p':
                tablero = hacerTablero(data[3], 9)
            elif respuestaDificultad.lower() == 'a':
                tablero = hacerTablero(data[3], 16)
            imprimirTablero(tablero)
            print()
            print()
            print(data[2])
            fila = input("Fila: ")
            columna = input("Columna: ")
            TCPClientSocket.sendall("{}-{}-{}-{}".format(fila, columna, respuestaDificultad, "j").encode())
        elif len(data[0]) == 0 and len(data[1]) == 0 and len(data[2]) > 0 and len(data[3]) > 0 and len(data[4]) == 0:
            if respuestaDificultad.lower() == 'p':
                tablero = hacerTablero(data[3], 9)
            elif respuestaDificultad.lower() == 'a':
                tablero = hacerTablero(data[3], 16)
            imprimirTablero(tablero)
            print()
            print()
            print(data[2])
            fila = input("Fila: ")
            columna = input("Columna: ")
            TCPClientSocket.sendall("{}-{}-{}-{}".format(fila, columna, respuestaDificultad, "j").encode())
        elif len(data[0]) == 0 and len(data[1]) == 0 and len(data[2]) == 0 and len(data[3]) > 0 and len(data[4]) > 0:
            if respuestaDificultad.lower() == 'p':
                tablero = hacerTablero(data[3], 9)
            else:
                tablero = hacerTablero(data[3], 16)
            imprimirTablero(tablero)
            print("¡Has ganado!\nTiempo de juego: " + data[4])
            juego = False
        else:
            if respuestaDificultad.lower() == 'p':
                tablero = hacerTablero(data[3], 9)
            else:
                tablero = hacerTablero(data[3], 16)
            imprimirTablero(tablero)
            print("\n\n¡Has perdido!\nTiempo de juego: " + data[4])
            juego = False
