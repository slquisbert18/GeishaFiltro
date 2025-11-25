from pathlib import Path
from datetime import datetime
from utils.obtenerCaracteristicas import *

# ****************** BUSQUEDAS GLOBALES (SISTEMA) ****************************
#              (trabaja con toda una ruta especificada)
def busqueda_global_color(colorInput, dataset, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in dataset.items():
        #print(f"{clave}:{valor}")
        # verificamos si se cancelo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
        fondo = valor.get('fondo')
        if isinstance(fondo, str) and colorInput.lower() in fondo.lower():
            resultados[clave] = valor
    return resultados
    
def busqueda_global_rgb(inputRGB, datos, cancelarCallBack = None):
    resultados = {}
    for clave, valor in datos.items():

        if cancelarCallBack and cancelarCallBack():
            return resultados

        if inputRGB in valor["rgb"]:
            resultados[clave] = valor
    return resultados

def busqueda_global_hex(inputHEX, datos, cancelarCallBack = None):
    resultados = {}
    codHex = ""
    if '#' not in codHex:
        codHex = f"#{codHex}"

    for clave in list(datos.keys()):

        if cancelarCallBack and cancelarCallBack():
            return resultados
        metaDatos = datos[clave]
        if inputHEX in metaDatos["hex"]:
            resultados[clave] = metaDatos
    return resultados

def busqueda_global_tamanio(tamanioInput, datos, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in datos.items():
        # verificamos si el usuario detuvo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
        
        if tamanioInput in valor["tamanio"]:
            resultados[clave] = valor
    
    return resultados

def busqueda_global_fecha(fechaInput, datos, cancelarCallBack = None): 
    resultados = {}
    for clave, valor in datos.items():
        if cancelarCallBack and cancelarCallBack():
            return resultados
        diccionarioFechas = valor["fecha"]
        if len(diccionarioFechas) == 1:
            if fechaInput in diccionarioFechas["DateTime"]:
                resultados[clave] = valor
        else:
            for valor in diccionarioFechas.values():
                if fechaInput in valor:
                    resultados[clave] = valor
                    break

    return resultados
   
def busqueda_global_nombre(nombreInput, datos, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in datos.items():
        # verificamos si el usuario detuvo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
        
        if nombreInput in (valor["nombre"] + valor["formato"]):
            resultados[clave] = valor
    
    return resultados
    