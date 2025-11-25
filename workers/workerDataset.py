from PySide6.QtCore import QObject, Signal
from utils.fileUtils import armarDiccionario
class WorkerDataset(QObject):
    progreso = Signal(int)
    finalizado = Signal(dict)
    error = Signal(str)

    def __init__(self, ruta):
        super().__init__()
        self.ruta = ruta

    def run(self):
        try:
            dataset = armarDiccionario(self.ruta, self.progreso)
            self.finalizado.emit(dataset)
        except Exception as e:
            self.error.emit(str(e))