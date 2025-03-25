import json
import os
import hashlib
from datetime import datetime

class commit:
    def __init__(self, correo, mensaje, rama, archivo=None, commit_siguiente=None, id=None, fecha=None):
        # Inicialización de atributos del commit
        self.commit_siguiente = commit_siguiente  # Referencia al siguiente commit
        self.timestamp = datetime.now().isoformat() if fecha is None else datetime.fromisoformat(fecha)
        self.correo = correo  # Correo del autor
        self.mensaje = mensaje  # Mensaje del commit
        self.rama = rama  # Rama asociada
        
        # Generación del ID único del commit usando SHA1
        if commit_siguiente is None:
            self.id = hashlib.sha1((f"None{self.timestamp}{self.correo}{self.correo}{self.rama}").encode('utf-8')).hexdigest()
        else:
            self.id = hashlib.sha1((f"{self.commit_siguiente.id}{self.timestamp}{self.correo}{self.correo}{self.rama}").encode('utf-8')).hexdigest()
        
        # Si se proporciona un ID explícito, usarlo
        if id is not None:
            self.id = id
            
        # Archivos asociados al commit
        self.archivos = f"{self.id}_archivos.json"
        self.archivo = []
        
        # Cargar archivos si no se proporcionan
        if archivo is None:
            self.descargar_archivo()
        else:
            self.cargar_archivos(archivo)

    def descargar_archivo(self):
        """Carga los archivos asociados desde el archivo JSON"""
        if os.path.exists(self.archivos):
            with open(self.archivos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["archivos"]:
                archivo_cargada = Archivo(r["nombre"], r["peso"])
                self.archivo.append(archivo_cargada)

    def cargar_archivos(self, archivos):
        """Guarda los archivos en el archivo JSON"""
        datos = {"archivos": []}
        if os.path.exists(self.archivos):
            with open(self.archivos, 'r') as archivo:
                datos = json.load(archivo)
                
        for archivo in archivos:
            nueva_archivo = {
                "nombre": archivo.nombre,
                "peso": archivo.peso,
            }
            datos["archivos"].append(nueva_archivo)
            
        with open(self.archivos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

class Archivo:
    """Clase que representa un archivo en el sistema"""
    def __init__(self, nombre, peso):
        self.nombre = nombre  # Nombre del archivo
        self.peso = peso  # Peso en bytes
        self.contenido = "documento"  # Contenido por defecto

class lista_commit:
    """Clase que maneja la lista de commits de una rama"""
    def __init__(self, rama, repositorio):
        self.estado = None
        self.cabeza = None  # Primer commit de la lista
        self.datos = "sinGuardar.json"  # Archivo para cambios no confirmados
        self.rama = rama  # Nombre de la rama
        self.datos_commit = f"{repositorio}_{rama}_commit.json"  # Archivo de commits
        
        # Inicialización de archivos JSON si no existen
        if not os.path.exists(self.datos):
            datos = {"Archivo": []}
            with open(self.datos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)

        if not os.path.exists(self.datos_commit):
            datos = {"commit": []}
            with open(self.datos_commit, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        else:
            self.descargar_commit()  # Cargar commits existentes

    def agregar_commit(self, c, carga=None):
        """Añade un commit a la lista"""
        if carga is not None:
            self.cargar_commit(c)
            
        if not self.cabeza:
            self.cabeza = c
        else:
            actual = self.cabeza
            while actual.commit_siguiente:
                actual = actual.commit_siguiente
            actual.commit_siguiente = c

    def descargar_commit(self):
        """Carga los commits desde el archivo JSON"""
        if os.path.exists(self.datos_commit):
            with open(self.datos_commit, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["commit"]:
                c = commit(r["correo"], r["mensaje"], self.rama, None, None, r["id"], r["fecha"])
                self.agregar_commit(c)

    def cargar_commit(self, commit):
        """Guarda un commit en el archivo JSON"""
        with open(self.datos_commit, 'r') as archivo:
            datos = json.load(archivo)

        nuevo_commit = {
            "id": commit.id,
            "correo": commit.correo,
            "mensaje": commit.mensaje,
            "fecha": commit.timestamp.isoformat() if hasattr(commit.timestamp, 'isoformat') else commit.timestamp,
        }
        datos["commit"].append(nuevo_commit)
        with open(self.datos_commit, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def git_add(self, nombre, peso):
        """Añade archivos al área de staging"""
        with open(self.datos, 'r') as archivo:
            datos = json.load(archivo)
            
        nueva_Archivo = {
            "nombre": nombre,
            "peso": peso,
        }
        datos["Archivo"].append(nueva_Archivo)
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def git_commit(self):
        """Crea un nuevo commit con los cambios en staging"""
        with open(self.datos, 'r') as archivo:
            datos = json.load(archivo)
            
        archivos = [Archivo(arch["nombre"], arch["peso"]) for arch in datos["Archivo"]]
        
        correo = input("Ingrese el correo: ")
        mensaje = input("Ingrese el mensaje: ")
        c = commit(correo, mensaje, self.rama, archivos)
        self.agregar_commit(c, "Nuevo")
        
        # Limpiar el área de staging
        datos = {"Archivo": []}
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def git_log(self):
        """Muestra el historial de commits"""
        actual = self.cabeza
        while actual:
            print("Commit ID:", actual.id)
            print()
            actual = actual.commit_siguiente

    def git_merge(self, nombre, repositorio):
        """Fusiona dos ramas de commits"""
        try:
            listaMerge = lista_commit(nombre, repositorio)
            actual1 = listaMerge.cabeza
            actual2 = self.cabeza
            cola = None
            
            # Buscar el punto de divergencia
            while actual1.commit_siguiente is not None or actual2.commit_siguiente is not None:
                if actual1.id != actual2.id:
                    cola = actual2
                if actual2.commit_siguiente is not None:
                    actual2 = actual2.commit_siguiente
                if actual1.commit_siguiente is not None:
                    actual1 = actual1.commit_siguiente
            
            # Realizar la fusión
            prueba = listaMerge.cabeza
            while prueba.commit_siguiente:
                prueba = prueba.commit_siguiente
            prueba.commit_siguiente = cola
            
            # Guardar los cambios fusionados
            datos = {"commit": []}
            with open(self.datos_commit, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
                
            prueba = listaMerge.cabeza
            while prueba:
                self.cargar_commit(prueba)
                prueba = prueba.commit_siguiente
        except Exception as e:
            print(f"Error en merge: {e}")

    def git_status(self, nombre, repositorio):
        """Muestra el estado actual del repositorio"""
        print("Archivos por subir:")
        if os.path.exists(self.datos):
            with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)
            if datos["Archivo"]:
                for r in datos["Archivo"]:
                    print(f"Nombre: {r['nombre']}")
                    print(f"Peso: {r['peso']}")
                    print()
            else:
                print("No hay archivos por subir")
                
        print(f"Repositorio: {repositorio}")
        print(f"Rama actual: {nombre}")
        
        
