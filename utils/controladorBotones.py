from datetime import datetime
from PySide6.QtCore import QThread, QDate
from modelos.modeloImagenes import imagenesModel
from workers.workerBusqueda import Worker
from utils.controladorHistorial import guardar_historial
from utils.ventanasFlotantes import avisoFlotante

class controladorBusqueda():
    def __init__(self, main, datos):
        self.main = main
        self.hilo = None
        self.Worker = None

    def buscar(self):
        ui = self.main.ui

        # limpiamos los mensajes de estatus al presionar de nuevo el boton de buscar
        ui.fondoStatus.setText(" ")
        ui.tamanioStatus.setText(" ")
        ui.fechaStatus.setText(" ")
        ui.nombreStatus.setText(" ")
        ui.hexStatus.setText(" ")
        ui.rgbStatus.setText(" ")
        ui.foto.clear()
        
        # mostramos la barra de carga
        ui.statusbar.showMessage("Filtrado en proceso...")

        # ***************** obtenemos los datos *************************
        # obtenemos la fecha
        fechaRecogida = ui.dateEdit.date()

        # si la fecha es igual a 2000/1/1, es porque no se introdujo ninguna fecha
        if fechaRecogida == datetime(2000, 1, 1):
            fechaRecogida = ""
        else:
            fechaRecogida = fechaRecogida.toString("yyyy:MM:dd") 

        # diccionario donde guardaremos los filtros
        filtros = {}

        # recogemos los datos de los lineEdit
        def guardarInputs(le, clave):
            if le.text() != "":
                # recogemos el valor del input
                valor = le.text().lower()

                # guardamos el input en el historial
                guardar_historial(self.main, le, valor)

                # guardamos la clave y el valor en el diccionario
                filtros[clave] = valor

        guardarInputs(ui.leFondo, "fondo")
        # antes de guardar el tamanio, verificamos si el usuario uso una coma en lugar de punto (para valores decimales)
        tamanioFinal = ""
        if ui.leTamanio.text() != "":
            tamanioFinal = ui.leTamanio.text()
            if ',' in tamanioFinal:
                tamanioFinal = ui.leTamanio.text().replace(',', '.')
            filtros["tamanio"] = tamanioFinal
        guardarInputs(ui.leNombreArchivo, "nombre")
        guardarInputs(ui.leHex, "hex")
        guardarInputs(ui.leRgb, "rgb")
        
        if fechaRecogida != "":
            filtros["fecha"] = fechaRecogida
        
        # filtramos la lista de filtros sacando los filtros vacios
        if not filtros:
            avisoFlotante("AVISO", "Debe ingresar al menos un valor", tipo = "advertencia", parent=self.main, )
            return

        # ********************** creacion del hilo y el worker ***********************
        self.hiloBusqueda = QThread()
        self.workerBusqueda = Worker(
            self.main.ruta, 
            filtros, 
            datasetCallback = lambda : self.main.dataset)
        self.workerBusqueda.moveToThread(self.hiloBusqueda)
        
        # verificacion de hilos
        if hasattr(self, "workerBusqueda") and self.workerBusqueda is not None:
            if self.hiloBusqueda is not None and self.hiloBusqueda.isRunning():
                self.workerBusqueda.cancelar = True
        

        # conexiones
        self.hiloBusqueda.started.connect(self.workerBusqueda.run)
        self.workerBusqueda.finished.connect(self.main.recibirResultados)
        self.workerBusqueda.finished.connect(self.hiloBusqueda.quit)
        self.workerBusqueda.finished.connect(self.workerBusqueda.deleteLater) # el objeto Qthread se destruye cuando termina
        self.hiloBusqueda.finished.connect(self.limpiarHilo)

        # conexion para actualizar los labels desde el worker
        self.workerBusqueda.status_update.connect(self.main.actualizar_label_status)

        self.hiloBusqueda.start()
    
    def detener(self):
        if self.hiloBusqueda is not None and self.hiloBusqueda.isRunning():
            self.workerBusqueda.cancelar = True
            self.main.ui.statusbar.showMessage("Búsqueda detenida")  
    
    def reiniciar(self):
        ui = self.main.ui
        ui.leFondo.clear()
        ui.fondoStatus.setText(" ")

        ui.leTamanio.clear()
        ui.tamanioStatus.setText(" ")

        ui.dateEdit.setDate(QDate(2000, 1, 1))
        ui.fechaStatus.setText(" ")

        ui.leNombreArchivo.clear()
        ui.nombreStatus.setText(" ")

        ui.leHex.clear()
        ui.hexStatus.setText(" ")

        ui.leRgb.clear()
        ui.rgbStatus.setText(" ")

        ui.resultadosDeBusqueda.setModel(imagenesModel({}, icon_size=100))
        ui.foto.clear()
        self.pixmap_original = None

        # eliminamos el contenido de una lista
        self.main.resultados.clear()

        ui.tableMetaDatos.clear()
        ui.statusbar.showMessage("")
        
    def limpiarHilo(self):
        self.hiloBusqueda = None
        self.workerBusqueda = None
        self.main.ui.statusbar.showMessage(f"Busqueda finalizada: {len(self.main.resultados)} encontrados")