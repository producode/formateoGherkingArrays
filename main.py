import pandas as pd
import numpy
import json

csvreader = pd.read_csv("./formateo.csv", index_col=0)
NIVEL = "Nivel "
nivelMaximo = 10
nombre = NIVEL + str(1)
objeto = {}


def elegirTipo(csv, nivel, posicion):
    nombre = NIVEL + str(nivel)
    if "(array)" in csv[nombre][posicion]:
        return "array"
    elif type(csv[NIVEL + str(nivel + 1)][posicion + 1]) != type(numpy.float64(1)) and type(csv[NIVEL + str(nivel + 1)][posicion + 1]) != type(float(1)):
        return "objeto"
    else:
        return "str"


def esElFinal(csv, posicionAVerificar, nivelMax):
    for i in range(1, nivelMax):
        if type(csv[NIVEL + str(i)][posicionAVerificar]) != type(float(1)) and type(csv[NIVEL + str(i)][posicionAVerificar]) != type(numpy.float64(1)):
            return False
    return True

def constructorString(objetosNivel):
    nombres = "| codigo | descripcion | "
    datos =   "| ok     | caso ok     | "
    for posicion in range(len(objetosNivel[0])):
        cantidadEspacios = len(str(objetosNivel[1][posicion])) - len(str(objetosNivel[0][posicion]))
        nombres += str(objetosNivel[0][posicion])
        datos += str(objetosNivel[1][posicion])
        if cantidadEspacios > 0:
            nombres += (" "*cantidadEspacios) + " | "
            datos += " | "
        elif cantidadEspacios < 0:
            datos += (" " * (cantidadEspacios * (-1))) + " | "
            nombres += " | "
        else:
            nombres += " | "
            datos += " | "
    return nombres, datos


ultimoObjeto = [objeto]
objetosNivel1 = [[], []]
for i in range(len(csvreader[nombre])):
    print(csvreader)
    if esElFinal(csvreader, i, nivelMaximo):
        break

    for nivelActual in range(1, nivelMaximo):
        nombre = NIVEL + str(nivelActual)
        if type(csvreader[nombre][i]) != type(float(1)) and type(csvreader[nombre][i]) != type(numpy.float64(1)):
            tipo = elegirTipo(csvreader, nivelActual, i)

            nombreObjetoModificado = csvreader[nombre][i].replace("(array)", "")
            if tipo == "array":
                ultimoObjeto[nivelActual-1][nombreObjetoModificado] = [{}]
            elif tipo == "objeto":
                ultimoObjeto[nivelActual-1][nombreObjetoModificado] = {}
            else:
                ultimoObjeto[nivelActual-1][nombreObjetoModificado] = str(csvreader["OK"][i])
            if len(ultimoObjeto) <= nivelActual:
                ultimoObjeto.append(ultimoObjeto[nivelActual-1][nombreObjetoModificado])
            else:
                ultimoObjeto[nivelActual] = ultimoObjeto[nivelActual-1][nombreObjetoModificado]
            if nivelActual == 1:
                objetosNivel1[0].append(nombreObjetoModificado)
                objetosNivel1[1].append(ultimoObjeto[1])
            if tipo == "array":
                ultimoObjeto[nivelActual] = ultimoObjeto[nivelActual][0]

            break

nombres, datos = constructorString(objetosNivel1)

print(objetosNivel1)
print(json.dumps(objeto, indent=2))
print("+" + "-"*(len(nombres)-3) + "+")
print(nombres)
print(datos)
print("+" + "-"*(len(nombres)-3) + "+")

