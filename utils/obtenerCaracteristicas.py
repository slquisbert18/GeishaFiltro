import cv2
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from pathlib import Path
import numpy as np
import os
from datetime import datetime

# ***************************************************************************
def leer_rutas(ruta_str):
    try:
        # convertimos la cadena a un objeto Path
        ruta = Path(ruta_str)

        # normalizamos la ruta
        ruta = ruta.resolve()

        # verifica si el archivo de la ruta existe
        if not ruta.exists():
            print(f"ERROR Archivo inexistente o corrupto: {ruta}")
            return None
        
        # verifica si obtenemos un archivo (y no asi una carpeta)
        if not ruta.is_file():
            print(f"ERROR archivo no valido: {ruta}")
            return None
        return ruta
    
    except (OSError, ValueError) as e:
        print(f"Error al procesar la ruta {ruta}: {e}")
        return None

# ****************** OBTENCION DE DATOS DE UNA IMAGEN ************************
# funcion para obtener el tamanio de la imagen
def obtener_tamanio(nombre):
    ruta_imagen = leer_rutas(nombre)
    if ruta_imagen is None:
        return None, None
    else: 
        imagen = cv2.imread(str(ruta_imagen))
        if imagen is None: 
            return None, None
        else: 
            alto_px, ancho_px, canales = imagen.shape

            # convertimos los pixeles a centimetros
                # obtenemos el PPP o DPI
            imagen_info = Image.open(nombre)
            if "dpi" in imagen_info.info:
                dpi = imagen_info.info['dpi']
                dpi_valor = dpi[0]
                # calculamos las dimensiones en cm
                ancho_cm = (ancho_px/dpi_valor) * 2.54
                alto_cm = (alto_px/dpi_valor) * 2.54

            else:
                # colocamos valores por defecto a dpi = 900, ancho_cm y alto_cm
                dpi = 900
                ancho_cm = (ancho_px/dpi) * 2.54
                alto_cm = (alto_px/dpi) * 2.54
            
            tamanio = str(f"{round(ancho_cm, 1)}x{ round(alto_cm, 1)}")
            if '.0' in tamanio:
                tamanio = tamanio.replace(".0", "")
            return tamanio 


# funcion para obtener la fecha
def obtener_fecha(nombre):
    nombre_imagen = leer_rutas(nombre)

    if nombre_imagen is None:
        print("Error al leer el nombre de la imagen")
        return None
    else:
        fechas = {}    
        imagen_info = Image.open(nombre)

        # obtenemos datos exif de la imagen
        try:
            datos_exif = imagen_info._getexif()
            if not datos_exif:
                # en caso de que la imagen no tenga metadatos disponibles, devolvemos la fecha de creacion del archivo
                fechaAux = os.path.getctime(nombre_imagen)
                fechaAux = datetime.fromtimestamp(fechaAux)
                fechaAux = fechaAux.strftime("%Y:%m:%d")
                fechas['DateTime'] = fechaAux
                return fechas
            # guardamos todas las fechas disponibles en los datos exif
            """
            APLICACION DESARROLLADA POR: Sergio Luis Quisbert Lopez CI: 9168790LP
            fecha y hora (fh)
            DateTimeOriginal: fh en que se tomo la foto
            DateTimeDigitalized: fh en la que la imagen fue digitalizada
            DateTime: fh de la ultima modificacion del archivo
            FileModifyDate/FileCreateDate: si se encuentra presente se almacena (no siempre disponible)
            """
            for etiqueta_id, value in datos_exif.items():
                etiqueta = ExifTags.TAGS.get(etiqueta_id, etiqueta_id)
                if type(etiqueta) is str and "Date" in etiqueta:
                    fechas[etiqueta] = value[:10]
                    
            """
            if fechas:
                for etiqueta, valor in fechas.items():
                    print(f"{etiqueta}: {valor[:10]}")
            else:
                print("No se encontro la fecha de creacion del archivo")
            """
            return fechas

        except AttributeError:
            print("El formato de la imagen no contiene metadatos EXIF")

# funcion para determinar si el fondo de una imagen corresponde al color 'color_base'
def obtenerFondo(ruta_imagen, umbral_porcentaje = 80):

    # definimos rangos de colores
    colores = {
        "rojo_1": ((0,   100, 100),  (10,  255, 255)),
        "rojo_2": ((178, 150, 130),  (179, 255, 255)),
        "verde":  ((35,  40,  40),  (85,  255, 255)),
        "azul":   ((100,  120,  80),  (120, 255, 255)),
        "celeste":((80,  20, 100),  (105, 255, 255)),
        "guindo": ((160, 100, 30),  (179, 255, 200)),
        "amarillo":((20, 50, 100),  (35, 255, 255)),
        "blanco": ((0, 0, 230),  (179, 20, 255)),
        "plomo": ((0, 0, 40), (179, 30, 220))
    }
    # abrimos la imagen
    img = cv2.imread(ruta_imagen)

    # si no se pudo cargar la imagen devolvemos false
    if img is None:
        return False
    
    # Si la imagen se abrio entonces tomamos una porcion de ella 
    x, y, ancho, alto = 0, 0, 20, 20
    zona_fondo = img[y:y+alto, x:x+ancho]

    # convertimos ese pedazo a HSV, es mas preciso que RGB
    hsv = cv2.cvtColor(zona_fondo, cv2.COLOR_BGR2HSV)

    # variables para comparar colores
    colorFondo = None
    porcentajeMax = 0

    # iteramos sobre los colores del diccionario
    for nombre, (rangoMin, rangoMax) in colores.items():
        # si es rojo unimos las dos mascaras
        if nombre.startswith("rojo"):
            if nombre == "rojo_1":
                rango1_min, rango1_max = colores["rojo_1"]
                rango2_min, rango2_max = colores["rojo_2"]

                # creamos mascaras separadas para luego unirlas
                mascara1 = cv2.inRange(hsv, np.array(rango1_min), np.array(rango1_max))
                mascara2 = cv2.inRange(hsv, np.array(rango2_min), np.array(rango2_max))
                mascara_total = cv2.bitwise_or(mascara1, mascara2)

                nombre = "rojo"

            else:
                continue # ya que rojo_2 esta considerado en rojo_1
        else:
            mascara_total = cv2.inRange(hsv, np.array(rangoMin), np.array(rangoMax))

        # calculo de porcentaje de pixeles del color x
        porcentaje = (cv2.countNonZero(mascara_total) / mascara_total.size) * 100

        # si porcentaje es mayor al 80% guardamos el color y porcentaje
        if porcentaje > porcentajeMax:
            porcentajeMax = porcentaje
            colorFondo = nombre
    
    # verificamos si el color supera el umbral
    if porcentajeMax >= umbral_porcentaje:
        return colorFondo
    else: 
        return None

# obtener el codigo rgb/hex de una imagen
def obtener_hex(nombre):
    ruta_archivo = leer_rutas(nombre)
    if ruta_archivo is None:
        return None
    imagen = cv2.imread(str(nombre))

    if imagen is None:
        return None
    
    # convertimos la imagen de BGR a RGB
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # elegimos una zona del fondo
    """
    x: coordenada x
    y: coordenada y
    ancho, alto: tamanio area
    """
    x, y, ancho, alto = 0, 0, 20, 20
    zona_fondo = imagen_rgb[y:y+alto, x:x+ancho]

    # calculamos el color promedio de esa zona
    color_promedio = np.mean(zona_fondo.reshape(-1, 3), axis=0)
    r, g, b = [int(c) for c in color_promedio] 

    # convertimos a formato HEX
    color_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    #print(f"Color de fondo en RGB: {r}, {g}, {b}")
    #print(f"Color de fondo en HEX: {color_hex}")

    return color_hex

# obtencion de metadatos de una imagen teniendo la ruta de la misma
def obtener_metadatos(ruta_imagen):
    img = Image.open(ruta_imagen)
    exif_data = img.getexif()
    metadatos = {}

    # nombre del archivo
    metadatos['Nombre'] = os.path.basename(ruta_imagen)

    # formato de imagen
    metadatos['Formato'] = img.format

     # dpi
    metadatos['DPI'] = img.info.get('dpi', (None, None))  #(dpi_x, dpi_y)

    # Tamaño en pixeles
    ancho_px, alto_px = img.size
    metadatos['Ancho (px)'] = ancho_px
    metadatos['Alto (px)'] = alto_px

    # tamanio en cm
    try:
        metadatos['Ancho (cm)'], metadatos['Alto (cm)'] = obtener_tamanio(ruta_imagen).split('x')
    except:
        metadatos['Ancho (cm)'] = None
        metadatos['Alto (cm)'] = None

    # rgb y hex
    hex = obtener_hex(ruta_imagen) 
    metadatos['Color HEX'] = hex
    
    # copyright y artista desde EXIF
    if exif_data:
        for tag_id, valor in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in ['Copyright', 'Artist']:
                metadatos[tag] = valor

        # 8️⃣ Fechas: Fecha de creación o modificación
        for tag_id, valor in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
                metadatos[tag] = valor
    if exif_data:
        for etiquetaId, valor in exif_data.items():
            etiqueta = TAGS.get(etiquetaId, etiquetaId)
            metadatos[etiqueta] = str(valor)
    return metadatos


#print(obtenerFondo("C:\\Users\\Sergio Quisbert\\Desktop\\PROYECTOS\\AppGeisha\\imagenes\\verde7.jpeg"))
#print(obtener_hex("C:\\Users\\Sergio Quisbert\\Desktop\\PROYECTOS\\AppGeisha\\imagenes\\3x3_MATE\\2_022128 copia.jpg"))