import json
import os
from pathlib import Path

def guardarDiccionario(rutaArchivo, diccionario):
    rutaArchivo = Path(rutaArchivo)
    with rutaArchivo.open("w", encoding="utf-8") as f:
        json.dump(diccionario, f, indent=4, ensure_ascii=False)

def cargarDiccionario(rutaArchivo):
    if not os.path.exists(rutaArchivo): # si no existe
        return None
    if os.path.getsize(rutaArchivo) == 0: # si el archivo esta vacio
        return None

    with open(rutaArchivo, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # archivo corrupto o contenido inválido
            return {}
