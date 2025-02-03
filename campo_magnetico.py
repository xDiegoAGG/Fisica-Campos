#En este archivo se calcula el campo Magnetico de la espira sobre todos los puntos

import utilidades as ut  #Se usa el archivo con las funciones

espacio = ut.crearEspacio()  #Se define el espacio

#Se definen los vertices de la espira
A = (0.2, 0, 0.2)
B = (-0.2, 0, 0.2)
C = (-0.2, 0, -0.2)
D = (0.2, 0, -0.2)

separacionDLs = 0.04 #Separación elegida entre un dL y otro

segmentos_corriente = []

for punto_inicio, punto_final in [(A, B), (B, C), (C, D), (D, A)]:  #Se usa un ciclo para guardar los vectores dL
    segmento = ut.crearListaPuntos(punto_inicio, punto_final, separacionDLs)
    for i in range(len(segmento) - 1):
        inicio = segmento[i]
        final = segmento[i + 1]
        dl = ut.calcularVectorAB(inicio, final)
        segmentos_corriente.append((inicio, dl))

corriente_total = 12e-3 #Corriente total en la espira

I_por_segmento = corriente_total / len(segmentos_corriente)
segmentos_corriente = [(I_por_segmento, inicio, dl) for inicio, dl in segmentos_corriente]

ut.graficarDLs(espacio, [seg[1] for seg in segmentos_corriente], [seg[2] for seg in segmentos_corriente], color="yellow")  #Se grafican los diferenciales en el espacio

vectores_campo_magnetico = []
separacionPuntosPiso = 0.2

for i in range(-5, 6):  #Se calculan los campos magneticos en cada punto
    x = i * 0.2
    segPiso = ut.crearListaPuntos((x, 1, 0), (x, -1, 0), separacionPuntosPiso)

    for punto in segPiso:
        campo_total = ut.calcularCampoMagneticoTotal(punto, segmentos_corriente)
        vectores_campo_magnetico.append((punto, campo_total))

ut.graficarVectores(espacio, [p[0] for p in vectores_campo_magnetico], [p[1] for p in vectores_campo_magnetico])  #Se graifcan los vectores de campo Magnetico

ut.mostrarEspacio() #Se muestra el espacio

matriz_x, matriz_y, matriz_z = ut.extraer_matrices_coordenadas(vectores_campo_magnetico)


#Por último se extraen las coordenadas de los vectores y se imprimen las matrices correspondientes

print("A continuación las coordenadas en X de los vectores de campo magnético:\n")
print(matriz_x)
print("\nA continuación las coordenadas en Y de los vectores de campo magnético:\n")
print(matriz_y)
print("\nA continuación las coordenadas en Z de los vectores de campo magnético:\n")
print(matriz_z)