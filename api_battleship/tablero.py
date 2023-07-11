import numpy as np


def colocar_barco(tablero, tamanio, orientacion, y, x):
    """
    Función que verifica si se puede colocar el barco y lo hace

    :param tablero: tablero en juego
    :param tamanio: tamaño del barco a colocar
    :param orientacion: en qué dirección se ubicará el barco a partir del punto inicial
    :param y: fila del punto inicial a partir del cual colocar el barco
    :param x: columna del punto inicial a partir del cual colocar el barco

    :return: True en caso de se haya  ubicado el barco en la orientación y coordinadas dadas.
             False en caso contrario.
    """

    ancho = tablero.shape[0]
    alto = tablero.shape[1]

    if (orientacion == 'N') and (y >= alto-tamanio-1):
        if np.all(tablero[y-tamanio+1:y+1, x] == ' '):
            tablero[y-tamanio+1:y+1, x] = str(tamanio)
            return True

    elif (orientacion == 'S') and (y <= alto-tamanio):
        if np.all(tablero[y:y+tamanio, x] == ' '):
            tablero[y:y+tamanio, x] = str(tamanio)
            return True

    elif (orientacion == 'E') and (x <= ancho-tamanio):
        if np.all(tablero[y, x:x+tamanio] == ' '):
            tablero[y, x:x+tamanio] = str(tamanio)
            return True

    elif (orientacion == 'O') and (x >= tamanio-1):
        if np.all(tablero[y, x-tamanio+1:x+1] == ' '):
            tablero[y, x-tamanio+1:x+1] = str(tamanio)
            return True
    else:
        return False


def posicionar_barco_aleatorio(tablero, tamanio):
    """
    Función que genera coordenadas y orientación aleatorias y llama a la función colocar_barco para que verifique si se
    puede colocar con esas variables y lo hace en caso positivo

    :param tablero: tablero en el que posicionar y colocar el barco
    :param tamanio: tamaño del barco
    """

    ancho = tablero.shape[0]
    alto = tablero.shape[1]

    barco_colocado = False

    while not barco_colocado:
        orientacion = np.random.choice(list('NSOE'))
        y, x = np.random.randint(alto), np.random.randint(ancho)
        barco_colocado = colocar_barco(tablero, tamanio, orientacion, y, x)
        if barco_colocado:
            break


def crea_tablero_usuario(ancho, alto):
    """
    Función que genera un tablero (matriz numpy de strings) con 10 barcos. El posicionamiento del barco se hará según
    coordenadas y orientación aleatorias.

    - 1 portaaviones que ocupa 4 espacios
    - 2 acorazados que ocupan 3 espacios cada uno
    - 3 fragatas que ocupan 2 espacios cada una
    - 4 submarinos que ocupan 1 espacio cada uno
    """

    tablero = np.full((alto, ancho), ' ')
    barcos = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    for barco in barcos:
        posicionar_barco_aleatorio(tablero, barco)

    return tablero
