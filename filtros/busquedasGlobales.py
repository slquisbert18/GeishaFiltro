from pathlib import Path
from datetime import datetime
from utils.obtenerCaracteristicas import *
from utils.fileUtils import busquedaPorNombreAvanzada

# ****************** BUSQUEDAS GLOBALES (SISTEMA) ****************************
#              (trabaja con toda una ruta especificada)
def busqueda_global_color(colorInput, dataset, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in dataset.items():
        # verificamos si se cancelo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
        archivoFondo = valor.get('fondo')
        if not archivoFondo:
            continue
        if isinstance(archivoFondo, str) and colorInput.lower() in archivoFondo.lower():
            resultados[clave] = valor
    return resultados

def busqueda_global_hex(inputHEX, datos, cancelarCallBack = None):
    resultados = {}
    codHex = ""
    if '#' not in codHex:
        codHex = f"#{codHex}"

    for clave, valor in datos.items():

        if cancelarCallBack and cancelarCallBack():
            return resultados
        archivoHex = valor.get("hex")

        if not archivoHex:
            continue
        
        if inputHEX.lower() in archivoHex.lower():
            resultados[clave] = valor
    return resultados

def busqueda_global_tamanio(tamanioInput, datos, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in datos.items():
        # verificamos si el usuario detuvo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
        
        archivoTamanio = valor.get("tamanio")
        
        if not archivoTamanio:
            continue
        
        if tamanioInput.lower() in archivoTamanio.lower():
            resultados[clave] = valor
    
    return resultados

def busqueda_global_fecha(fechaInput, datos, cancelarCallBack = None): 
    resultados = {}
    for clave, valor in datos.items():
        if cancelarCallBack and cancelarCallBack():
            return resultados
        
        diccionarioFechas = valor.get("fecha")

        # si el diccionario no tiene fechas, lo saltamos
        if not diccionarioFechas:
            continue
        
        for fecha in diccionarioFechas.values():
            if not fecha:
                continue
            if fechaInput in fecha:
                resultados[clave] = valor
                break

    return resultados

# filtros teniendo un rango de fecha para buscar
def filtroMes(inputMes, datos):
    resultados = {}
    for clave, valor in datos.items():
        diccionarioFechas = valor.get("fecha")
        if not diccionarioFechas:
            continue
        for fecha in diccionarioFechas.values():
            # como tenemos fechas de tipo -> YYYY:MM:DD
            anio, mes, dia = fecha.split(":")
            if int(inputMes) == int(mes):
                resultados[clave] = valor
                break # si encontramos una fecha coincidente cortamos el recorrido del diccionario de fechas
    return resultados

def filtroMesAnio(inputMes, inputAnio, datos):
    resultados = {}
    for clave, valor in datos.items():
        diccionarioFechas = valor.get("fecha")
        if not diccionarioFechas:
            continue
        for fecha in diccionarioFechas.values():
            # como tenemos fechas de tipo -> YYYY:MM:DD
            anio, mes, dia = fecha.split(":")
            if int(inputMes) == int(mes) and inputAnio == anio:
                resultados[clave] = valor
                break # si encontramos una fecha coincidente cortamos el recorrido del diccionario de fechas
    return resultados

def filtroMesesAnio(inputMesIni, inputMesFin, inputAnio, datos):
    resultados = {}
    for clave, valor in datos.items():
        diccionarioFechas = valor.get("fecha")
        if not diccionarioFechas:
            continue
        for fecha in diccionarioFechas.values():
            # como tenemos fechas de tipo -> YYYY:MM:DD
            anio, mes, dia = fecha.split(":")
            if int(mes) >= int(inputMesIni) and int(mes) <= int(inputMesFin) and inputAnio == anio:
                resultados[clave] = valor
                break # si encontramos una fecha coincidente cortamos el recorrido del diccionario de fechas
    return resultados

def filtroMeses(inputMesIni, inputMesFin, datos):
    resultados = {}
    for clave, valor in datos.items():
        diccionarioFechas = valor.get("fecha")
        if not diccionarioFechas:
            continue
        for fecha in diccionarioFechas.values():
            # como tenemos fechas de tipo -> YYYY:MM:DD
            anio, mes, dia = fecha.split(":")
            if int(mes) >= int(inputMesIni) and int(mes) <= int(inputMesFin):
                resultados[clave] = valor
                break # si encontramos una fecha coincidente cortamos el recorrido del diccionario de fechas
    return resultados   

def filtroAnio(inputAnio, datos):
    resultados = {}
    for clave, valor in datos.items():
        diccionarioFechas = valor.get("fecha")
        if not diccionarioFechas:
            continue
        for fecha in diccionarioFechas.values():
            # como tenemos fechas de tipo -> YYYY:MM:DD
            anio, mes, dia = fecha.split(":")
            if anio == inputAnio:
                resultados[clave] = valor
                break # si encontramos una fecha coincidente cortamos el recorrido del diccionario de fechas
    return resultados         
   
def busqueda_global_nombre(inputArchivo, datos, cancelarCallBack = None):
    # lista de resultados
    resultados = {}
    
    for clave, valor in datos.items():
        # verificamos si el usuario detuvo la busqueda
        if cancelarCallBack and cancelarCallBack():
            return resultados
 
        nombreArchivo = valor.get("nombre") + valor.get("formato")

        if busquedaPorNombreAvanzada(nombreArchivo, inputArchivo):
            resultados[clave] = valor
    
    return resultados