from PySide6.QtWidgets import QMessageBox

# funcion para mostrar mensajes en una ventana emergente
def avisoFlotante(titulo, mensaje, tipo="info", parent=None):
    msg = QMessageBox(parent)
    msg.setWindowTitle(titulo)
    msg.setText(mensaje)

    if tipo == "info":
        msg.setIcon(QMessageBox.Information)
    elif tipo == "advertencia":
        msg.setIcon(QMessageBox.Warning)
    elif tipo == "error":
        msg.setIcon(QMessageBox.Critical)
    msg.exec()