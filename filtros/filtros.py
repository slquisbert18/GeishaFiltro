from datetime import datetime
from utils.obtenerCaracteristicas import *
import copy


# ****************** BUSQUEDAS TENIENDO UNA LISTA ****************************
def filtrar_por_tamanio(resultados, inputDimension):
    resultado = {}
    for clave in list(resultados.keys()):
        datos = resultados[clave]
        dimensionArchivo = datos["tamanio"]
        if inputDimension.lower() in dimensionArchivo.lower():
            resultado[clave] = datos
    return resultado

def filtrar_por_fondo(resultados, inputFondo):
    resultado = {}
    for clave in list(resultados.keys()):
        datos = resultados[clave]
        fondoArchivo = datos["fondo"]
        if inputFondo.lower() in fondoArchivo.lower():
            resultado[clave] = datos
    return resultado

def filtrar_por_fecha(resultados, inputFecha):    
    resultado = {}
    for clave in list(resultados.keys()):
        datos = resultados[clave]
        diccionarioFechas = datos["fecha"]

        for valor in diccionarioFechas.values():
            if inputFecha in valor:
                resultado[clave] = datos
                break
    return resultado
    

def filtrar_por_nombre(resultados, inputNombre):
    resultado = {}
    for clave in list(resultados.keys()):
        datos = resultados[clave]
        nombreArchivo = datos["nombre"]

        # si el nombre introducido no esta en el nombre extraido, se elimina de la lista
        if inputNombre.lower() in nombreArchivo.lower():
            resultado[clave] = datos
            
    return resultado

def filtrar_por_hex(resultados, inputCodHEX):
    resultado = {}
    for clave in list(resultados.keys()):
        datos = resultados[clave]
        hexArchivo = datos["hex"]
        if inputCodHEX.lower() in hexArchivo.lower():
            resultado[clave] = datos
    return resultado



            

