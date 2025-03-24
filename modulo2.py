import json
import os
import hashlib
from datetime import datetime

class commit:
    def __init__(self,correo,mensaje,rama,archivo=None,commit_siguiente=None,id=None,fecha=None):
        self.commit_siguiente=commit_siguiente
        if fecha==None:
            self.timestamp = datetime.now().isoformat()
        else:
            self.timestamp= datetime.fromisoformat(fecha)
        self.correo=correo
        self.mensaje=mensaje
        self.rama=rama
        #
        if commit_siguiente == None:
            self.id=hashlib.sha1((f"None{self.timestamp}{self.correo}{self.correo}{self.rama}").encode('utf-8')).hexdigest()
        else:
            self.id=hashlib.sha1((f"{self.commit_siguiente.id}{self.timestamp}{self.correo}{self.correo}{self.rama}").encode('utf-8')).hexdigest()
        if id != None:
            self.id=id
        self.archivos=f"{self.id}_archivos.json"
        #
        self.archivo=[]
        if archivo==None:
            self.descargar_archivo()
        else:
            self.cargar_archivos(archivo)

    def descargar_archivo(self):

        if os.path.exists(self.archivos):
            with open(self.archivos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["archivos"]:
                archivo_cargada= Archivo(r["nombre"],r["peso"])
                self.archivo.append(archivo_cargada)

    def cargar_archivos(self,archivos):
        if os.path.exists(self.archivos):
            with open(self.archivos, 'r') as archivo:
                    datos = json.load(archivo)
        else:
            datos = {"archivos": []}
        for archivo in archivos:
                nombre=archivo.nombre
                peso=archivo.peso
                nueva_archivo={
                    "nombre": nombre,
                    "peso":peso,
                }
                datos["archivos"].append(nueva_archivo)     
        with open(self.archivos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
class Archivo:
    def __init__(self,nombre,peso):
        self.nombre=nombre
        self.peso=peso
        self.contenido="documento"

class lista_commit:
    def __init__(self,rama,repositorio):
        self.estado=None
        self.cabeza = None
        self.datos = "sinGuardar.json"
        if not os.path.exists(self.datos):
           datos = {"Archivo": []}
           with open(self.datos, 'w') as archivo:
               json.dump(datos, archivo, indent=4)

        self.rama=rama
        self.datos_commit=f"{repositorio}_{rama}_commit.json"
        if not os.path.exists(self.datos_commit):
           datos = {"commit": []}
           with open(self.datos_commit, 'w') as archivo:
               json.dump(datos, archivo, indent=4)
        else:
            self.descargar_commit()
        
    #
    def agregar_commit(self,c,carga=None):
        nuevo_nodo = c
        if carga !=None:
            self.cargar_commit(nuevo_nodo)
        if not self.cabeza:
            self.cabeza = c
        else:
            actual = self.cabeza
            while actual.commit_siguiente:
                actual = actual.commit_siguiente
            actual.commit_siguiente = c

    def descargar_commit(self):

        if os.path.exists(self.datos_commit):
            with open(self.datos_commit, 'r') as archivo:
                print("aqui")
                datos = json.load(archivo)
            for r in datos["commit"]:
                print(r["fecha"])
                c=commit(r["correo"],r["mensaje"],self.rama,None,None,r["id"],r["fecha"])
                self.agregar_commit(c)
    
    def cargar_commit(self,commit):

        with open(self.datos_commit, 'r') as archivo:
                datos = json.load(archivo)

        nuevo_commit={
            "id": commit.id,
            "correo": commit.correo,
            "mensaje":commit.mensaje,
            "fecha":commit.timestamp.isoformat() if hasattr(commit.timestamp, 'isoformat') else commit.timestamp,
        }
        datos["commit"].append(nuevo_commit)     
        with open(self.datos_commit, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def git_add(self,nombre,peso):
        with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)
        nueva_Archivo={
            "nombre": nombre,
            "peso":peso,
        }
        datos["Archivo"].append(nueva_Archivo)     
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def git_commit(self):
        with open(self.datos, 'r') as archivo:
            datos = json.load(archivo)
        archivos=[]
        for arch in datos["Archivo"]:
            archivos.append(Archivo(arch["nombre"],arch["peso"]))
        #
        correo=input("ingrese el correo")
        mensaje=input("ingrese el mensaje")
        c=commit(correo,mensaje,self.rama,archivos)
        self.agregar_commit(c,"Nuevo")
        datos = {"Archivo": []}
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        
    def git_log(self):
        actual = self.cabeza
        while actual:
            print("Nombre:", actual.id)
            print()
            actual = actual.commit_siguiente
    
    def git_merge(self,nombre,repositorio):
        listaMerge=lista_commit(nombre,repositorio)
        actual1 = listaMerge.cabeza
        actual2 = self.cabeza
        cola=None
        bandera=1
        while actual1.commit_siguiente!=None or actual2.commit_siguiente!=None:
            print("hola")
            if actual1.id!=actual2.id:
                cola=actual2
            else:
                print("igual")
            if actual2.commit_siguiente != None:
                actual2 = actual2.commit_siguiente
            if actual1.commit_siguiente != None:
                actual1 = actual1.commit_siguiente
        prueba = listaMerge.cabeza

        while prueba.commit_siguiente:
            prueba = prueba.commit_siguiente
        prueba.commit_siguiente = cola
        prueba = listaMerge.cabeza

        datos = {"commit": []}
        with open(self.datos_commit, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
        while prueba:
            print("Nombre:", prueba.mensaje)
            self.cargar_commit(prueba)
            prueba = prueba.commit_siguiente

    def git_status(self,nombre,repositorio):
        print("Archivos por subir")
        if os.path.exists(self.datos):
            with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)
            if len(datos["Archivo"])!=0:
                for r in datos["Archivo"]:
                    print(f"nombre: {r["nombre"]}")
                    print(f"peso: {r["peso"]}")
                    print()
            else:
                print("No hay archivos por subir")
        print(f"El nombre del repositorio es{repositorio}")
        print(f"El nombre de la rama  es{nombre}")
        
        
        
        
