from PySide6.QtWidgets import QListWidget, QListWidgetItem, QLineEdit
from PySide6.QtCore import Qt, QPoint, QEvent


#********************** MANEJO DE UN POPUP PARA EL HISTORIAL ***********************
class PopUpHistorial(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # para que no bloquee los demas elementos
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)

        self.lineEditActual = None

        # aca va el estilo
        
        #self.setSpacing(0)
        #self.setContentsMargins(0, 0, 0, 0)
        #self.setStyleSheet("""
        #    QListWidget {
        #        background: #1e1e1e;
        #        color: #f0f0f0;
        #        font-size: 13px;
        #        padding: 2px;
        #        border: 1px solid #555;
        #   }
        #    QListWidget::item {
        #        padding: 3px 6px;
        #    }
        #    QListWidget::item:hover {
        #        background: #333;
        #    }
        #""")

        self.itemClicked.connect(self.seleccionar)

    # mostrar el popup debajo de un LineEdit
    def mostrar(self, lineEdit, historial):
        self.clear()

        limite = 5 # cantidad maxima de items a mostrar
        itemsAMostrar = historial[:limite]

        for h in historial[:limite]:
            self.addItem(QListWidgetItem(h))

        self.lineEditActual = lineEdit

        # posicion debajo de un lineEdit
        pos = lineEdit.mapToGlobal(QPoint(0, lineEdit.height()))
        self.move(pos)
        
        self.setFixedWidth(lineEdit.width())

        # calcular altura dinámica
        item_count = len(itemsAMostrar)
        if item_count == 0:
            self.hide()
            return
        
        alturaItem = self.sizeHintForRow(0) # altura de un item
        altura_total = min(item_count, limite) * alturaItem+2 * self.frameWidth()
        self.setMaximumHeight(altura_total) # aproximadamente 5 elementos
        self.adjustSize()
        
        self.show()
        self.setFocus()

    # coloca el historial en el LineEdit
    def seleccionar(self, item):
        if self.lineEditActual:
            self.lineEditActual.setText(item.text())
        self.hide()

    # cuando se oculta limpiamos la referencia
    #def hideEvent(self, event):
    #    self.lineEditActual = None
    #    return super().hideEvent(event)

    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)

    def recolocar(self):
        if self.lineEditActual:
            posicion = self.lineEditActual.mapToGlobal(QPoint(0, self.lineEditActual.height()))
            self.move(posicion)
# para colocar un elemento del historial en el lineEdit
def colocar_en_le(self, index):
    texto = self.ui.cbHistorial.itemText(index)
    if hasattr(self, "lineEditActual"):
        self.lineEditActual.setText(texto)
    self.ui.cbHistorial.hide()

# *********************** HISTORIAL Y AUTOCOMPLETADO ******************************
# guardamos los elementos del lineEdit al hacer clic en el boton buscar
def guardar_historial(self, lineEdit, texto):
    if not texto:
        return
       
    clave = f"historial_{lineEdit.objectName()}"

    # cargamos el historial anterior
    historial = self.settings.value(clave, [])

    # evitamos duplicados y agregar al inicio
    if texto not in historial:
        historial.insert(0, texto)

    # guardamos en QSettings (maximo 5 elementos)
    self.settings.setValue(clave, historial[:5])
    

# mostrar el historial cuando sea llamado
def mostrar_historial(self, lineEdit):
    clave = f"historial_{lineEdit.objectName()}"
    historial = self.settings.value(clave, [])
    self.popup.mostrar(lineEdit, historial)
    """
    clave = f"historial_{lineEdit.objectName()}"
    historial = self.settings.value(clave, [])

    self.ui.cbHistorial.clear()
    self.ui.cbHistorial.addItems(historial)
      
    # calcula la posicion debajo del lineEdit
    pos = lineEdit.mapTo(self, QPoint(0, lineEdit.height()))
    self.ui.cbHistorial.move(pos)
    self.ui.cbHistorial.setFixedWidth(lineEdit.width())
        
    #mostramos todos los elementos
    self.ui.cbHistorial.raise_()
    self.ui.cbHistorial.show()
    #self.ui.cbHistorial.showPopup()

    # guardamos una referencia del LineEdit actual
    self.lineEditActual = lineEdit
        """

