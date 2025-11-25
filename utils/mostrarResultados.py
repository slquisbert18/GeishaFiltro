from PySide6.QtWidgets import QHeaderView, QTableWidgetItem
from PySide6.QtGui import QPixmap, Qt
import os
from utils.obtenerCaracteristicas import obtener_metadatos

# ******************** FUNCIONES PARA MOSTRAR ICONOS E IMAGENES *********************
def mostrar_imagen(self, index):
    ruta_completa = index.data(Qt.UserRole) # obtenemos solo el nombre del archivo

    if isinstance(ruta_completa, str) and os.path.exists(ruta_completa):
        # obtenemos los metadatos de la imagen en un diccionario
        metadatos = obtener_metadatos(ruta_completa)

        # llamamos a una funcion para mostrar los metadatos en una tabla
        mostrar_metadatos(self, metadatos)

        self.pixmap_original = QPixmap(ruta_completa) # guardamos el pixmap original para que cuando aumente el tamano del layout, el original crezca 
        if self.pixmap_original.isNull():
            print("no se pudo cargar la imagen en QPixmap")
            return 
        actualizar_imagen(self)
    else:
        print("Imagen no encontrada")

def actualizar_imagen(self):
    if self.pixmap_original and not self.pixmap_original.isNull():
        pixmap_scaled = self.pixmap_original.scaled(
            self.ui.foto.width(),
            self.ui.foto.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.ui.foto.setPixmap(pixmap_scaled)

# funcion para mostrar los datos en una Tabla
def mostrar_metadatos(self, metadatos):
    tabla = self.ui.tableMetaDatos
    tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tabla.clear()
    tabla.setRowCount(len(metadatos))
    tabla.setColumnCount(2)
    tabla.setHorizontalHeaderLabels(["Atributo", "Valor"])

    for fila, (clave, valor) in enumerate(metadatos.items()):
        tabla.setItem(fila, 0, QTableWidgetItem(str(clave)))
        tabla.setItem(fila, 1, QTableWidgetItem(str(valor)))

    tabla.resizeColumnsToContents