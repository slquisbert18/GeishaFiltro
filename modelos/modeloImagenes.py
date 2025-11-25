from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QPixmap, QIcon
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

        if role == Qt.DisplayRole:
            return os.path.basename(ruta)

        if role == Qt.DecorationRole:
            if ruta not in self.cache:
                pixmap = QPixmap(ruta).scaled(
                    self.icon_size, self.icon_size,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.cache[ruta] = QIcon(pixmap)
            return self.cache[ruta]

        if role == Qt.UserRole:
            return ruta