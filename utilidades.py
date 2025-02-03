#Se crea una clase utilidades con funciones que se usan para la implementación de los calculos

import numpy as np
import matplotlib.pyplot as plt  #Se importan las librerias numpy y matplotlib para el gráfico

def crearEspacio(): #Función que nos ayuda a generar el gráfico
    fig = plt.figure()
    espacio = fig.add_subplot(111, projection='3d')

    lim = 2

    espacio.set_xlim([-lim, lim])
    espacio.set_ylim([-lim, lim])
    espacio.set_zlim([-lim, lim])

    espacio.quiver(0, 0, 0, 0, lim, 0, color="red", arrow_length_ratio=0.1)
    espacio.quiver(0, 0, 0, 0, -lim, 0, color="red", arrow_length_ratio=0.1)
    espacio.quiver(0, 0, 0, lim, 0, 0, color="green", arrow_length_ratio=0.1)
    espacio.quiver(0, 0, 0, -lim, 0, 0, color="green", arrow_length_ratio=0.1)
    espacio.quiver(0, 0, 0, 0, 0, lim, color="blue", arrow_length_ratio=0.1)
    espacio.quiver(0, 0, 0, 0, 0, -lim, color="blue", arrow_length_ratio=0.1)

    espacio.set_xlabel("X")
    espacio.set_ylabel("Z")
    espacio.set_zlabel("Y")

    ticks = np.arange(-lim, lim + 1, 1)
    espacio.set_xticks(ticks)
    espacio.set_yticks(ticks)
    espacio.set_zticks(ticks)

    espacio.grid(True)

    return espacio
def graficarPuntos(espacio, puntos): #Función para graficar distintos puntos en el espacio
    for x, y, z in puntos:
        espacio.scatter(x, y, z, color='yellow', s=25)
def graficarVectores(espacio, puntos, vectores): #Función para graficar vectores en el espacio
    for (px, py, pz), (vx, vy, vz) in zip(puntos, vectores):
        espacio.quiver(px, py, pz, vx, vy, vz, length=1, normalize=True)
def graficarDLs(espacio, puntos, vectores, color='yellow'): #Función especifica para graficar los diferenciales de longitud en la espira de campo magnetico
    for (px, py, pz), (vx, vy, vz) in zip(puntos, vectores):
        espacio.quiver(px, py, pz, vx, vy, vz, length=1, normalize=True, color=color)
def mostrarEspacio(): #Muestra el espacio generado
    plt.show()
def calcularVectorAB(A, B): #Función para calcular el vector de un punto a otro
    return (B[0] - A[0], B[1] - A[1], B[2] - A[2])
def distanciaAB(A, B): #Función para la distancia entre dos puntos
    return ((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2 + (B[2] - A[2]) ** 2) ** 0.5
def normaVector(v): #Función que nos devuelve la norma de un vector
    return (v[0] ** 2 + v[1] ** 2 + v[2] ** 2) ** 0.5
def vectorUnitario(A, B): #Función para hallar el vector unitario de un punto a otro
    vectorAB = calcularVectorAB(A, B)
    norma = normaVector(vectorAB)
    if norma == 0:
        return (0, 0, 0)
    r_unitario = (vectorAB[0] / norma, vectorAB[1] / norma, vectorAB[2] / norma)
    return r_unitario
def calcularCampoElectricoPuntual(Q, distancia, unitario): #Función para calcular el campo electrico en un punto P por una sola carga
    k = 8.99e9
    magnitud = k * Q / distancia**2
    vectorCampo = (magnitud * unitario[0], magnitud * unitario[1], magnitud * unitario[2])
    return vectorCampo
def calcularCampoElectricoTotal(puntoP, cargas): #Función para calcular el campo producido por todas las cargas de la espira
    campo_total = (0, 0, 0)

    for Q, posicion in cargas:
        distancia = distanciaAB(posicion, puntoP)
        if distancia == 0:
            continue
        unitario = vectorUnitario(posicion, puntoP)
        campo_electrico = calcularCampoElectricoPuntual(Q, distancia, unitario)
        campo_total = (campo_total[0] + campo_electrico[0],
                       campo_total[1] + campo_electrico[1],
                       campo_total[2] + campo_electrico[2])
    return campo_total
def crearListaPuntos(punto_inicial, punto_final, separacion):  #Función para crear una lista con puntos de un segmento
    distancia = distanciaAB(punto_inicial, punto_final)
    num_puntos = int(distancia / separacion)
    puntos = []
    for i in range(num_puntos + 1):
        punto = (punto_inicial[0] + i * (punto_final[0] - punto_inicial[0]) / num_puntos,
                 punto_inicial[1] + i * (punto_final[1] - punto_inicial[1]) / num_puntos,
                 punto_inicial[2] + i * (punto_final[2] - punto_inicial[2]) / num_puntos)
        puntos.append(punto)
    return puntos
def extraer_matrices_coordenadas(vectores):  #Función para separar las coordenadas de los vectores
    x_coords = [vector[1][0] for vector in vectores]
    y_coords = [vector[1][1] for vector in vectores]
    z_coords = [vector[1][2] for vector in vectores]

    n = int(np.sqrt(len(vectores)))
    matriz_x = np.array(x_coords).reshape(n, n)
    matriz_y = np.array(y_coords).reshape(n, n)
    matriz_z = np.array(z_coords).reshape(n, n)

    return matriz_x, matriz_y, matriz_z
def calcularCampoMagneticoSegmento(I, dl, punto_segmento, punto_calculo):  #Función para calcular el campo Magnetico producido por un solo diferencia de longitud o de corriente
    MU_0 = 4 * np.pi * 1e-7
    r = calcularVectorAB(punto_segmento, punto_calculo)
    distancia = distanciaAB(punto_segmento, punto_calculo)

    if distancia == 0:
        return (0, 0, 0)

    dl_x_r = (dl[1] * r[2] - dl[2] * r[1], dl[2] * r[0] - dl[0] * r[2], dl[0] * r[1] - dl[1] * r[0])

    coeficiente = MU_0 * I / (4 * np.pi * distancia ** 3)
    campo_magnetico = (coeficiente * dl_x_r[0], coeficiente * dl_x_r[1], coeficiente * dl_x_r[2])
    return campo_magnetico
def calcularCampoMagneticoTotal(puntoP, segmentos_corriente):  #Función para calcular el campo magnetico total generado por toda la espira en un punto P
    campo_total = (0, 0, 0)
    for I, punto_segmento, dl in segmentos_corriente:
        campo_magnetico = calcularCampoMagneticoSegmento(I, dl, punto_segmento, puntoP)
        campo_total = (campo_total[0] + campo_magnetico[0], campo_total[1] + campo_magnetico[1], campo_total[2] + campo_magnetico[2])
    return campo_total