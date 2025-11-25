from PySide6.QtCore import Qt

def eventosTeclas(main, event):
    # para que el boton ENTER active la funcion buscar()
    if event.key() in (Qt.Key_Return, Qt.Key_Enter):
        if event.modifiers() & Qt.ControlModifier: # verifica si esta pulsada la tecla ctrl
            main.ui.botonAbrir.click() # si es asi, se abre el archivo seleccionado en el explorador
        else:
            main.ui.botonBuscar.click() # si no es asi, solo se presiona el boton buscar 

    # para presionar el boton reset usaremos el DELETE
    if event.key() == Qt.Key_Delete:
        main.ui.botonReiniciar.click()
