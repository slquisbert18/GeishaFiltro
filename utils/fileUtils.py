from PySide6.QtGui import Qt
from pathlib import Path
import subprocess
from PySide6.QtCore import QItemSelectionModel
from utils.ventanasFlotantes import avisoFlotante
from utils.obtenerCaracteristicas import *

formatos = ('*.jpg','*.png', '*.jpeg', '*.psd', '*.raw') 

# cargar diccionario
def armarDiccionario(ruta):
    carpeta = Path(ruta)
    dataset = {} # usaremos un diccionario para almacenar diccionarios
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
                codigo rgb y hex
            """
            r, g, b, hex = obtener_rgb_hex(rutaArchivo) or (0,0,0,None) # devulve un codigo rgb: (XX, YY, ZZ)
            datosArchivo = {
                "nombre": archivo.name,
                "formato": archivo.suffix.lower(), # retorna el formato de la imagen: jpg, jpeg, etc.
                "fondo": obtenerFondo(rutaArchivo), # retorna el nombre del colore: "rojo", "azul", etc
                "tamanio": obtener_tamanio(rutaArchivo), # retorna una cadena: "AxB"
                "fecha": obtener_fecha(rutaArchivo), # devuelve un diccionario con las fechas disponibles
                "rgb": f"({r}, {g}, {b})",
                "hex": hex, 
            }

            # guardamos el diccionario de datos de la imagen en otro diccionario donde
            # clave: ruta de la imagen, valor: diccionario de datos
            dataset[rutaArchivo] = datosArchivo
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