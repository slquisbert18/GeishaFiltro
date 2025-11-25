from PySide6.QtCore import Signal, QObject
from filtros.filtros import *
from filtros.busquedasGlobales import *

class Worker(QObject):
    finished = Signal(dict) # emita la lista de imagenes encontradas
    status_update = Signal(str, str) # para emitir señales que serviran para mostrar mensajes en los labels
                                     # EN EL WORKER NO SE MANEJAN OBJETOS UI
    #resultadosParciales = Signal(list)

    def __init__(self, ruta, filtros, datasetCallback):
        super().__init__()
        self.ruta = ruta
        self.filtros = filtros.copy()
        self.datasetCallback = datasetCallback
        self.resultados = {}
        self.cancelar = False

    def run(self):
        # aca colocamos las funciones de busqueda
        copiaFiltros = self.filtros.copy()
        # si no se tiene ningun filtro terminamos la ejecucion del hilo
        if not copiaFiltros:
            self.finished.emit([])
            return
        
        # tomamos el primer criterio de busqueda
        primerFiltro, valor = next(iter(copiaFiltros.items()))
        datasetActual = self.datasetCallback()
        while not self.resultados and copiaFiltros:
            # verificamos que no se haya pulsado el boton de pararBusqueda
            if self.cancelar:
                self.finished.emit(self.resultados) # emitimos una lista con resultados parcial
                return
            
            # realizamos la primera busqueda global hasta que self.resultados tenga contenido
            if primerFiltro == "fondo":
                self.resultados = busqueda_global_color(
                    valor,
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("fondo", "Sin coincidencias")

            elif primerFiltro == "tamanio":
                #anchoAlto = valor.split('x')
                #ancho = round(float(anchoAlto[0]), 1)
                #alto = round(float(anchoAlto[1]), 1)
                self.resultados = busqueda_global_tamanio(
                    valor,
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("tamanio", "Sin coincidencias")
            
            elif primerFiltro == "fecha":
                self.resultados = busqueda_global_fecha(
                    valor,
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("fecha", "Sin coincidencias")
            
            elif primerFiltro == "nombre":
                self.resultados = busqueda_global_nombre(
                    valor,
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("nombre", "Sin coincidencias")

            elif primerFiltro == "hex":
                self.resultados = busqueda_global_hex(
                    valor,
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("hex", "Sin coincidencias")

            elif primerFiltro == "rgb":
                #texto = valor.replace('(', '').replace(')', '')
                #valores = texto.split(',')

                #r = int(valores[0].strip())
                #g = int(valores[1].strip())
                #b = int(valores[2].strip())

                self.resultados = busqueda_global_rgb(
                    valor.strip(),
                    datasetActual,
                    cancelarCallBack=lambda: self.cancelar
                )

                if not self.resultados:
                    self.status_update.emit("rgb", "Sin coincidencias")
            
            if not self.resultados:
                # si el primer filtro no consiguio resultados lo eliminamos de la copia de nuestro diccionario de filtros
                del copiaFiltros[primerFiltro]

                # verificamos que aun hayan elementos en copiaFiltros
                if not copiaFiltros:
                    break
                # tomamos el filtro que le sigue al filtro eliminado e intentamos nuevamente
                primerFiltro, valor = next(iter(copiaFiltros.items()))
            else:
                break
        
        # eliminamos el filtro que se uso para la busqueda global del diccionario de filtros
        del self.filtros[primerFiltro]

        # procedemos a hacer el filtro sobre la lista generada con la primera busqueda global
        if self.filtros:
            for filtro, valor in list(self.filtros.items()):
                # verificamos que no se haya pulsado el boton de pararBusqueda
                if self.cancelar:
                    self.finished.emit(self.resultados) # emitimos una lista vacia
                    return
                
                if filtro == "fondo":
                    resultadoFiltroFondo = filtrar_por_fondo(self.resultados, valor)
                    if self.resultados == resultadoFiltroFondo:
                        self.status_update.emit("fondo", "Mismas coincidencias")
                    elif not resultadoFiltroFondo:
                        self.status_update.emit("fondo", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroFondo
                
                elif filtro == "tamanio":
                    resultadoFiltroTamanio = filtrar_por_tamanio(self.resultados, valor)
                    if self.resultados == resultadoFiltroTamanio:
                        self.status_update.emit("tamanio", "Mismas coincidencias")
                    elif not resultadoFiltroTamanio:
                        self.status_update.emit("tamanio", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroTamanio
                
                elif filtro == "fecha":
                    resultadoFiltroFecha = filtrar_por_fecha(self.resultados, valor)
                    if self.resultados == resultadoFiltroFecha:
                        self.status_update.emit("fecha", "Mismas coincidencias")
                    elif not resultadoFiltroFecha:
                        self.status_update.emit("fecha", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroFecha

                elif filtro == "nombre":
                    resultadoFiltroNombre = filtrar_por_nombre(self.resultados, valor)
                    if self.resultados == resultadoFiltroNombre:
                        self.status_update.emit("nombre", "Mismas coincidencias")
                    elif not resultadoFiltroNombre:
                        self.status_update.emit("nombre", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroNombre       

                elif filtro == "hex":
                    resultadoFiltroHex = filtrar_por_hex(self.resultados, valor)
                    if self.resultados == resultadoFiltroHex:
                        self.status_update.emit("hex", "Mismas coincidencias")
                    elif not resultadoFiltroHex:
                        self.status_update.emit("hex", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroHex

                elif filtro == "rgb":
                    #texto = valor.replace('(', '').replace(')', '')
                    #valores = texto.split(',')

                    #r = int(valores[0].strip())
                    #g = int(valores[1].strip())
                    #b = int(valores[2].strip())
                    resultadoFiltroRgb = filtrar_por_rgb(self.resultados, valor)
                    if self.resultados == resultadoFiltroRgb:
                        self.status_update.emit("rgb", "Mismas coincidencias")
                    elif not resultadoFiltroRgb:
                        self.status_update.emit("rgb", "Sin coincidencias")
                    else:
                        self.resultados = resultadoFiltroRgb
     
        self.finished.emit(self.resultados)