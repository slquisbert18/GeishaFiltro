from PySide6.QtGui import Qt
from pathlib import Path
import subprocess
from PySide6.QtCore import QItemSelectionModel
from utils.ventanasFlotantes import avisoFlotante
from utils.obtenerCaracteristicas import *

formatos = ('*.jpg','*.png', '*.jpeg', '*.psd', '*.raw') 

# cargar diccionario
def armarDiccionario(ruta, senialProgreso = None):
    carpeta = Path(ruta)
    dataset = {} # usaremos un diccionario para almacenar diccionarios
    
    totalArchivos = sum(1 for formato in formatos for _ in carpeta.rglob(formato))
    progreso = 0
    
    for formato in formatos:
        for archivo in carpeta.rglob(formato):
            rutaArchivo = str(archivo)
            # de este archivo obtendremos los datos que nos interesan (solo para procesar los datos):
            """
                ruta (incluido nombre y formato) -> clave lo demas es valor 
                color de fondo
                ancho y alto en cm
                fecha de creacion
                nombre del archivo
                codigo hex
            """
            hex = obtener_hex(rutaArchivo)  # devulve un codigo hex: #000000
            datosArchivo = {
                "nombre": archivo.name,
                "formato": archivo.suffix.lower(), # retorna el formato de la imagen: jpg, jpeg, etc.
                "fondo": obtenerFondo(rutaArchivo), # retorna el nombre del colore: "rojo", "azul", etc
                "tamanio": obtener_tamanio(rutaArchivo), # retorna una cadena: "AxB"
                "fecha": obtener_fecha(rutaArchivo), # devuelve un diccionario con las fechas disponibles
                "hex": hex 
            }

            dataset[rutaArchivo] = datosArchivo

            # emitimos el progreso
            progreso += 1
            if senialProgreso:
                senialProgreso.emit(int(progreso / totalArchivos * 100))
            
            # guardamos el diccionario de datos de la imagen en un diccionario donde
            # clave: ruta de la imagen, valor: diccionario de datos
    return dataset

# funcion para abrir una imagen en el explorador
def mostrar_en_explorador(main):
    item = main.ui.resultadosDeBusqueda.currentIndex()
    if not item.isValid():
        avisoFlotante("Atención", "Ninguna imagen seleccionada", "advertencia", parent=main)
        return
    
    # recuperamos la ruta desde UserRole
    ruta = item.data(Qt.UserRole)
    
    if not ruta:
        avisoFlotante("Error", "No se pudo obtener la ruta", "error", parent=main)
        return
    # Seleccionamos explícitamente el item en el QListView
    main.ui.resultadosDeBusqueda.selectionModel().select(
        item, 
        QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
    )
    main.ui.resultadosDeBusqueda.setCurrentIndex(item)  # también lo establecemos como índice actual

    # Abrimos el explorador marcando la imagen
    subprocess.run(f'explorer /select,"{ruta}"')