#En este archivo se calcula el campo Electrico producido por una espira cuadrada en una región (Aproximadamente)

import utilidades as ut #Se usa el archivo con las funciones

espacio = ut.crearEspacio()  #Se crea el espacio

#Vertices de la espira
A = (0.2, 0, 0.2)
B = (-0.2, 0, 0.2)
C = (-0.2, 0, -0.2)
D = (0.2, 0, -0.2)
separacionCargas = 0.04  #Separación elegida entre una carga y otra

#Se parte la espira en 4 segmentos para facilitar los calculos

seg1Espira = ut.crearListaPuntos((0.16, 0, 0.2), B, separacionCargas)
seg2Espira = ut.crearListaPuntos((-0.2, 0, 0.16), C, separacionCargas)
seg3Espira = ut.crearListaPuntos((-0.16, 0, -0.2), D, separacionCargas)
seg4Espira = ut.crearListaPuntos((0.2, 0, -0.16), A, separacionCargas)

carga_por_segmento = 3e-9
cargas = []

for segmento in [seg1Espira, seg2Espira, seg3Espira, seg4Espira]:  #Se distribuye la carga entre los segmentos y las cargas
    carga_por_punto = carga_por_segmento / len(segmento)
    for punto in segmento:
        cargas.append((carga_por_punto, punto))


#Se grafican los puntos que representan las cargas puntuales

ut.graficarPuntos(espacio, seg1Espira)
ut.graficarPuntos(espacio, seg2Espira)
ut.graficarPuntos(espacio, seg3Espira)
ut.graficarPuntos(espacio, seg4Espira)

separacionPuntosPiso = 0.2
vectores_campo = []

for i in range(-5, 6):  #Se separa la zona a calcular el campo electrico y se calcula el campo
    x = i * 0.2
    segPiso = ut.crearListaPuntos((x, 1, 0), (x, -1, 0), separacionPuntosPiso)

    for punto in segPiso:
        campo_total = ut.calcularCampoElectricoTotal(punto, cargas)
        vectores_campo.append((punto, campo_total))

ut.graficarVectores(espacio, [p[0] for p in vectores_campo], [p[1] for p in vectores_campo])  #Se grafican los vectores de campo electrico
ut.mostrarEspacio()


#Se extraen las coordenadas de los vectores y se separan en matrices apartes paraposteriormente ser mostradas
matriz_x, matriz_y, matriz_z = ut.extraer_matrices_coordenadas(vectores_campo)

print("A continuación las coordenadas en X de los vectores de campo eléctrico:\n")
print(matriz_x)
print("\nA continuación las coordenadas en Y de los vectores de campo eléctrico:\n")
print(matriz_y)
print("\nA continuación las coordenadas en Z de los vectores de campo eléctrico:\n")
print(matriz_z)