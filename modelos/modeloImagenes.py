from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QPixmap, QIcon
from PIL import Image
import os

# MODELO PARA MOSTRAR LOS ITEMS EN EL QListView

class imagenesModel(QAbstractListModel):
    def __init__(self, diccionario, icon_size = 100):
        super().__init__()
        self.diccionarioResultados = diccionario # recibimos el diccinoario
        self.rutas = list(diccionario.keys()) # obtenemos las claves del diccionario en una lista
        self.icon_size = icon_size
        self.cache = {} # diccionario de miniaturas

    def rowCount(self, parent = QModelIndex()):
        return len(self.rutas)
    
    def data(self, index, role):
        if not index.isValid():
            return None
        
        ruta = self.rutas[index.row()]
        
        # nombre a mostrar
        if role == Qt.DisplayRole:
            return os.path.basename(ruta)
        
        # miniatura
        if role == Qt.DecorationRole:
            if ruta not in self.cache:
                extension = os.path.splitext(ruta)[1].lower() # obtenemos la extension del archivo
                # verificamos si la ruta apunta a un archivo psd
                if extension == ".psd":
                    try:
                        with Image.open(ruta) as img:
                            img = img.convert("RGB") # convertimos la image a png
                            rutaPsd = os.path.splitext(ruta)[0]
                            pngRuta = rutaPsd + "_temp.png"
                            img.save(pngRuta, "PNG") # crear y guardar el png temporal
                            rutaConvertida = pngRuta
                    except Exception as e:
                        print("Error:", e)
                        rutaConvertida = None
                else:
                    rutaConvertida = ruta
                                    
                if rutaConvertida and os.path.exists(rutaConvertida):
                    pixmap = QPixmap(ruta).scaled(
                        self.icon_size, self.icon_size,
                        Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                    self.cache[ruta] = QIcon(pixmap)
            return self.cache.get(ruta)

        if role == Qt.UserRole:
            return ruta
    def __del__(self):
        # borramos los png temporales de los archivos psd
        for ruta in list(self.cache.keys()):
            if ruta.endswith("_temp.png") and os.path.exists(ruta):
                try:
                    os.remove(ruta)
                except:
                    pass 