# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'principal.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QMainWindow,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 555)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.VerticalLayout = QVBoxLayout(self.centralwidget)
        self.VerticalLayout.setObjectName(u"VerticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.logo = QLabel(self.centralwidget)
        self.logo.setObjectName(u"logo")

        self.horizontalLayout_5.addWidget(self.logo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.horizontalLayout_5.addWidget(self.progressBar)

        self.botonExplorar = QPushButton(self.centralwidget)
        self.botonExplorar.setObjectName(u"botonExplorar")
        icon = QIcon()
        icon.addFile(u"../src/folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.botonExplorar.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.botonExplorar)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 2)
        self.horizontalLayout_5.setStretch(3, 1)

        self.VerticalLayout.addLayout(self.horizontalLayout_5)

        self.hlInputs = QHBoxLayout()
        self.hlInputs.setObjectName(u"hlInputs")
        self.layoutFondo = QVBoxLayout()
        self.layoutFondo.setObjectName(u"layoutFondo")
        self.labelFondo = QLabel(self.centralwidget)
        self.labelFondo.setObjectName(u"labelFondo")

        self.layoutFondo.addWidget(self.labelFondo)

        self.leFondo = QLineEdit(self.centralwidget)
        self.leFondo.setObjectName(u"leFondo")

        self.layoutFondo.addWidget(self.leFondo)

        self.fondoStatus = QLabel(self.centralwidget)
        self.fondoStatus.setObjectName(u"fondoStatus")

        self.layoutFondo.addWidget(self.fondoStatus)

        self.layoutFondo.setStretch(0, 2)
        self.layoutFondo.setStretch(2, 1)

        self.hlInputs.addLayout(self.layoutFondo)

        self.layoutTamanio = QVBoxLayout()
        self.layoutTamanio.setObjectName(u"layoutTamanio")
        self.labelTamanio = QLabel(self.centralwidget)
        self.labelTamanio.setObjectName(u"labelTamanio")

        self.layoutTamanio.addWidget(self.labelTamanio)

        self.leTamanio = QLineEdit(self.centralwidget)
        self.leTamanio.setObjectName(u"leTamanio")

        self.layoutTamanio.addWidget(self.leTamanio)

        self.tamanioStatus = QLabel(self.centralwidget)
        self.tamanioStatus.setObjectName(u"tamanioStatus")

        self.layoutTamanio.addWidget(self.tamanioStatus)

        self.layoutTamanio.setStretch(0, 2)
        self.layoutTamanio.setStretch(2, 1)

        self.hlInputs.addLayout(self.layoutTamanio)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelFecha = QLabel(self.centralwidget)
        self.labelFecha.setObjectName(u"labelFecha")

        self.verticalLayout.addWidget(self.labelFecha)

        self.dateEdit = QDateEdit(self.centralwidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.dateEdit)

        self.fechaStatus = QLabel(self.centralwidget)
        self.fechaStatus.setObjectName(u"fechaStatus")

        self.verticalLayout.addWidget(self.fechaStatus)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 1)

        self.hlInputs.addLayout(self.verticalLayout)

        self.layoutNombre = QVBoxLayout()
        self.layoutNombre.setSpacing(6)
        self.layoutNombre.setObjectName(u"layoutNombre")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.layoutNombre.addWidget(self.label)

        self.leNombreArchivo = QLineEdit(self.centralwidget)
        self.leNombreArchivo.setObjectName(u"leNombreArchivo")

        self.layoutNombre.addWidget(self.leNombreArchivo)

        self.nombreStatus = QLabel(self.centralwidget)
        self.nombreStatus.setObjectName(u"nombreStatus")

        self.layoutNombre.addWidget(self.nombreStatus)

        self.layoutNombre.setStretch(0, 2)
        self.layoutNombre.setStretch(1, 1)
        self.layoutNombre.setStretch(2, 1)

        self.hlInputs.addLayout(self.layoutNombre)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_7.addWidget(self.label_4)

        self.leHex = QLineEdit(self.centralwidget)
        self.leHex.setObjectName(u"leHex")

        self.verticalLayout_7.addWidget(self.leHex)

        self.hexStatus = QLabel(self.centralwidget)
        self.hexStatus.setObjectName(u"hexStatus")

        self.verticalLayout_7.addWidget(self.hexStatus)


        self.hlInputs.addLayout(self.verticalLayout_7)

        self.hlInputs.setStretch(0, 1)
        self.hlInputs.setStretch(1, 1)
        self.hlInputs.setStretch(2, 1)
        self.hlInputs.setStretch(3, 2)
        self.hlInputs.setStretch(4, 1)

        self.VerticalLayout.addLayout(self.hlInputs)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.botonBuscar = QPushButton(self.centralwidget)
        self.botonBuscar.setObjectName(u"botonBuscar")

        self.horizontalLayout_4.addWidget(self.botonBuscar)

        self.botonDetener = QPushButton(self.centralwidget)
        self.botonDetener.setObjectName(u"botonDetener")

        self.horizontalLayout_4.addWidget(self.botonDetener)

        self.botonReiniciar = QPushButton(self.centralwidget)
        self.botonReiniciar.setObjectName(u"botonReiniciar")

        self.horizontalLayout_4.addWidget(self.botonReiniciar)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)

        self.VerticalLayout.addLayout(self.horizontalLayout_4)

        self.splitterPrincipal = QSplitter(self.centralwidget)
        self.splitterPrincipal.setObjectName(u"splitterPrincipal")
        self.splitterPrincipal.setOrientation(Qt.Orientation.Horizontal)
        self.resultadosDeBusqueda = QListView(self.splitterPrincipal)
        self.resultadosDeBusqueda.setObjectName(u"resultadosDeBusqueda")
        self.splitterPrincipal.addWidget(self.resultadosDeBusqueda)
        self.panelCentral = QWidget(self.splitterPrincipal)
        self.panelCentral.setObjectName(u"panelCentral")
        self.vista = QVBoxLayout(self.panelCentral)
        self.vista.setObjectName(u"vista")
        self.vista.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.panelCentral)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 178, 323))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.foto = QLabel(self.scrollAreaWidgetContents)
        self.foto.setObjectName(u"foto")
        self.foto.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.foto)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2.setStretch(0, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.vista.addWidget(self.scrollArea)

        self.botonAbrir = QPushButton(self.panelCentral)
        self.botonAbrir.setObjectName(u"botonAbrir")

        self.vista.addWidget(self.botonAbrir)

        self.vista.setStretch(0, 1)
        self.vista.setStretch(1, 5)
        self.splitterPrincipal.addWidget(self.panelCentral)
        self.panelMetadatos = QWidget(self.splitterPrincipal)
        self.panelMetadatos.setObjectName(u"panelMetadatos")
        self.vlMetadatos = QVBoxLayout(self.panelMetadatos)
        self.vlMetadatos.setObjectName(u"vlMetadatos")
        self.vlMetadatos.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.panelMetadatos)
        self.label_2.setObjectName(u"label_2")

        self.vlMetadatos.addWidget(self.label_2)

        self.tableMetaDatos = QTableWidget(self.panelMetadatos)
        self.tableMetaDatos.setObjectName(u"tableMetaDatos")

        self.vlMetadatos.addWidget(self.tableMetaDatos)

        self.splitterPrincipal.addWidget(self.panelMetadatos)

        self.VerticalLayout.addWidget(self.splitterPrincipal)

        self.VerticalLayout.setStretch(0, 1)
        self.VerticalLayout.setStretch(1, 1)
        self.VerticalLayout.setStretch(2, 1)
        self.VerticalLayout.setStretch(3, 10)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.logo.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.botonExplorar.setText(QCoreApplication.translate("MainWindow", u"Carpeta raiz", None))
        self.labelFondo.setText(QCoreApplication.translate("MainWindow", u"Color de fondo:", None))
        self.fondoStatus.setText("")
        self.labelTamanio.setText(QCoreApplication.translate("MainWindow", u"Tama\u00f1o de la foto:", None))
        self.tamanioStatus.setText("")
        self.labelFecha.setText(QCoreApplication.translate("MainWindow", u"Fecha de registro:", None))
        self.fechaStatus.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Nombre del archivo:", None))
        self.leNombreArchivo.setInputMask("")
        self.leNombreArchivo.setText("")
        self.leNombreArchivo.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Nombre del archivo", None))
        self.nombreStatus.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"HEX", None))
        self.hexStatus.setText("")
        self.botonBuscar.setText(QCoreApplication.translate("MainWindow", u"BUSCAR", None))
        self.botonDetener.setText(QCoreApplication.translate("MainWindow", u"DETENER", None))
        self.botonReiniciar.setText(QCoreApplication.translate("MainWindow", u"LIMPIAR", None))
        self.foto.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.botonAbrir.setText(QCoreApplication.translate("MainWindow", u"ABRIR EN EL EXPLORADOR", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"INFORMACION DE LA IMAGEN", None))
    # retranslateUi

