from .principal import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QSizePolicy, QFileDialog, QLineEdit
from PySide6.QtCore import Qt, QSize, QDate, QSettings, QEvent, QTimer, QThread
from PySide6.QtGui import QPixmap, QFont

from modelos.modeloImagenes import imagenesModel
from utils.fileUtils import *
from utils.mostrarResultados import *
from utils.controladorHistorial import *
from utils.controladorBotones import controladorBusqueda
from utils.controladorTeclado import eventosTeclas
from workers.workerDataset import WorkerDataset


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # establecemos los tamanios de el espacio de resultados
        self.ui.splitterPrincipal.setStretchFactor(0, 30)
        self.ui.splitterPrincipal.setStretchFactor(1, 45)
        self.ui.splitterPrincipal.setStretchFactor(2, 25)
        QTimer.singleShot(0, lambda: self.ui.splitterPrincipal.setSizes([30, 45, 25]))

        # variables para guardar filtros y rutas
        self.dataset = {}
        self.resultados = {}
        self.pixmap_original = None
        self.ruta = ""
        self.lineEditActual = None

        # creamos un objeto QSettings
        self.settings = QSettings("Geisha", "AppGeisha")
        #self.cargar_ruta_seleccionada()
        rutaGuardada = self.settings.value("ruta_busqueda", "")
        if rutaGuardada:
            self.ruta = rutaGuardada
            self.cargarDataset(self.ruta)


        # **************************** logo ****************************************
        logo_png = QPixmap("src/logoMediano.jpg")
        self.ui.logo.setPixmap(logo_png)
        self.ui.logo.setScaledContents(True)

        # **************************** QListView ***********************************
        self.configurarListaResultados()

        # **************************** QLabel **********************************
        # el label donde se mostrara la imagen esta dentro de un verticalLayout
        self.configurarLabelImagen()

        # **************************** Botones ***********************************
        self.controlador = controladorBusqueda(self, self.dataset)
        
        self.ui.botonBuscar.clicked.connect(self.controlador.buscar)
        self.ui.botonReiniciar.clicked.connect(self.controlador.reiniciar)
        self.ui.botonDetener.clicked.connect(self.controlador.detener)
        self.ui.botonAbrir.clicked.connect(lambda: mostrar_en_explorador(self))
        self.ui.botonExplorar.clicked.connect(self.seleccionar_ruta)
        

        # conectamos el ListView con el label donde mostraremos la foto
        self.ui.resultadosDeBusqueda.clicked.connect(lambda index: mostrar_imagen(self, index))

        # *************************** calendario ********************************
        # colocamos una fecha invalida inicial (hasta el el usuario introduzca una)
        self.ui.dateEdit.setDate(QDate())

        # *********************** historial de busquedas ************************
        self.popup = PopUpHistorial(self)
        QApplication.instance().installEventFilter(self)

        # instalamos el eventFilter desde el inicio
        self.listaLineEdits = [
            self.ui.leFondo,
            self.ui.leTamanio,
            self.ui.leNombreArchivo,
            self.ui.leHex,
        ]
        for le in self.listaLineEdits:
            le.installEventFilter(self)

        
    def configurarListaResultados(self):
        # configuramos la fuente de los nombres de los resultados
        font = QFont()
        font.setPointSize(7)

        # Configuramos el QListView 
        self.ui.resultadosDeBusqueda.setFont(font) # aplicamos la fuente
        self.ui.resultadosDeBusqueda.setViewMode(QListView.IconMode) # configuramos el ListView para mostrar elementos como iconos
        self.ui.resultadosDeBusqueda.setIconSize(QSize(100, 100)) # tamano por defecto de los iconos
        self.ui.resultadosDeBusqueda.setResizeMode(QListView.Adjust) # para que los iconos se muevan de acuerdo al tamano del listView
        self.ui.resultadosDeBusqueda.setUniformItemSizes(True) # obliga a los elementos del ListView a tener el mismo tamanio
        self.ui.resultadosDeBusqueda.setWordWrap(False) # par que los nombres ocupen solo 1 linea 
    
    def configurarLabelImagen(self):
        # hacemos que el label contenedor de la imagen se expanda a todo el verticalLayout
        self.ui.foto.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding 
        )
        self.ui.foto.setMinimumSize(10, 10)
        self.ui.foto.setAlignment(Qt.AlignCenter) # para que la imagen se alinee al centro
        self.ui.foto.setScaledContents(False) # para que no se deforme la foto

    # ******************* FUNCIONES QUE TRABAJAN CON EL WORKER **************************
    def recibirResultados(self, resultados):
        self.resultados = resultados
        self.resultado_busqueda()

    def resultado_busqueda(self):    
        model = imagenesModel(self.resultados, icon_size=100)
        self.ui.resultadosDeBusqueda.setModel(model)

        # actualizamos la barra de estado
        if self.resultados:
            self.ui.statusbar.showMessage(f"Busqueda completada: {len(self.resultados)} elementos encontrados")
        else:
            self.ui.statusbar.showMessage("Busqueda completada: sin resultados")
    
    def actualizar_label_status(self, label, mensaje):
        if label == "fondo":
            self.ui.fondoStatus.setText(mensaje)
        elif label == "tamanio":
            self.ui.tamanioStatus.setText(mensaje)
        elif label == "fecha":
            self.ui.fechaStatus.setText(mensaje)
        elif label == "nombre":
            self.ui.nombreStatus.setText(mensaje)
        elif label == "hex":
            self.ui.hexStatus.setText(mensaje)
        elif label == "rgb":
            self.ui.rgbStatus.setText(mensaje)
    


    # ************************ FUNCION QUE TRABAJA CON EL SISTEMA **********************
    def cargarDataset(self, ruta):
        # limpiamos resultados previos
        self.resultados = {}
        self.ui.resultadosDeBusqueda.setModel(imagenesModel({}, icon_size=100))

        # creamos el worker para procesar el dataset
        self.hiloDataset = QThread()
        self.workerDataset = WorkerDataset(ruta)
        self.workerDataset.moveToThread(self.hiloDataset)

        # conexiones
        self.hiloDataset.started.connect(self.workerDataset.run)
        self.workerDataset.progreso.connect(self.ui.progressBar.setValue)
        self.workerDataset.finalizado.connect(self.datasetCargado)
        self.workerDataset.error.connect(lambda e: print("Error", e))
        self.workerDataset.finalizado.connect(self.hiloDataset.quit)
        self.workerDataset.finalizado.connect(self.workerDataset.deleteLater)
        self.hiloDataset.finished.connect(self.hiloDataset.deleteLater)

        self.hiloDataset.start()


    def seleccionar_ruta(self):
        ruta = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta raiz", # titulo del dialog
            self.ruta,
            QFileDialog.ShowDirsOnly # mostrar solo carpetas
        )

        if ruta: # si el usuario selecciono una carpeta
            self.settings.setValue("ruta_busqueda", ruta)
            self.ruta = ruta
            self.cargarDataset(self.ruta)


    def datasetCargado(self, dataset):
        self.dataset = dataset
        self.ui.progressBar.setValue(100)
        self.ui.statusbar.showMessage(f"Datos cargado: {len(dataset)} imagenes")

    def cargar_ruta_seleccionada(self):
        ruta = self.settings.value("ruta_busqueda", "")
        if ruta:
            self.ruta = ruta
            # cargamos el dataset
            self.dataset = armarDiccionario(self.ruta)
            self.resultados = {}
            self.ui.resultadosDeBusqueda.setModel(imagenesModel({}, icon_size=100))
        else:
            self.ruta = ""

    # ***************** EVENTOS **************************
    # para mostrar el combobox al hacer clic sobre el lineEdit
    def eventFilter(self, obj, event):
        if isinstance(obj, QLineEdit):
            if event.type() == QEvent.MouseButtonPress:
                # mostramos el historial si el objeto es un lineEdit
                mostrar_historial(self, obj)
                return False # evitamos que el evento se propague
        else:
            # si el popup es visible 
            if event.type() == QEvent.MouseButtonPress:
                if self.popup.isVisible():
                    if event.type() == QEvent.MouseButtonPress:
                        if not self.popup.geometry().contains(event.globalPos()) and \
                            not any(le.geometry().contains(event.globalPos()) for le in self.listaLineEdits):
                            self.popup.hide()
        return super().eventFilter(obj, event)
    
    # KEYPRESSEVENT
    def keyPressEvent(self, event):
        eventosTeclas(self, event)

    def resizeEvent(self, event):
        # cuando la ventana cambia de tamaño, actualizamos la imagen
        if hasattr(self, "pixmap_original") and self.pixmap_original:
            pixmap_scaled = self.pixmap_original.scaled(
                self.ui.foto.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.ui.foto.setPixmap(pixmap_scaled)
        
        try:
            self.popup.recolocar()
        except:
            pass
        super().resizeEvent(event)

    def moveEvent(self, event):
        try:
            self.popup.recolocar()
        except:
            pass
        super().moveEvent(event)