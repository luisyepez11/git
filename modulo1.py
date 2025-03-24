import json
import os

class Repositorio:
    def __init__(self,nombre):
        self.nombre=nombre
        self.ramas = []
        self.commit_resiente = None
        self.rama_actual = "main"
        self.rama_Principal = "main"
        self.ramasDatos = f"{nombre}.json"
        self.Repositorio_siguiente =None
        self.descargar_ramas()

    def crear_rama(self, nombre):
        if nombre=="":
            print("No ingresó ningún nombre")
        else:
            bandera=0
            for i in self.ramas:
                if nombre == i:
                    print("Ya hay una rama llamada así")
                    bandera=1
            if bandera==0:   
                rama = Rama(nombre,self.nombre)
                self.ramas.append(rama)
                self.cargar_ramas(rama)
                datos_commit=f"{self.nombre}_{self.rama_actual}_commit.json"
                with open(datos_commit, 'r') as archivo:
                    datos = json.load(archivo)
                datos_commit=f"{self.nombre}_{rama.nombre}_commit.json"
                with open(datos_commit, 'w') as archivo:
                    json.dump(datos, archivo, indent=4)
                print()
                print(f"Se creó una nueva rama {nombre}")
    
    def descargar_ramas(self):
        if os.path.exists(self.ramasDatos):
            with open(self.ramasDatos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["rama"]:
                rama_cargada= Rama(r['nombre'],self.nombre)
                self.ramas.append(rama_cargada)
            print("Descarga exitosa")
        else:
            commit=f"{self.nombre}_main_commit.js"
            datos = {"rama": []}
            rama = {
            "nombre": "main",
            "commit": commit,
            }
            datos["rama"].append(rama)
            with open(self.ramasDatos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        
    def cargar_ramas(self,rama):
        with open(self.ramasDatos, 'r') as archivo:
                datos = json.load(archivo)
        nombre=rama.nombre
        commit=rama.commit
        nueva_rama={
            "nombre": nombre,
            "commit":commit,
        }
        datos["rama"].append(nueva_rama)     
        with open(self.ramasDatos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
    def mostrarRamas(self):
        for i in self.ramas:
            print(i.nombre)
            
    def cambiarRama(self,nombre):
        cambio=0
        for i in self.ramas:
            if i.nombre==nombre:
                self.rama_actual=i.nombre
                cambio=1
        if cambio==0:
            print("No existe esa rama")


class Rama:
    def __init__(self, nombre,nombreRepositorio):
        self.nombre = nombre
        self.commit= f"{nombreRepositorio}_{nombre}_commit.js"

class Versiones:
    def __init__(self):
        self.cabeza = None
        self.datos = "DatosRepositorios.json"
        if not os.path.exists(self.datos):
            datos = {"Repositorios": []}
            with open(self.datos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
            print("ingrese el nombre del repositorio inicial")
            self.git_init()      
        self.descargarRepositorios()
        self.repositoriosActual=self.cabeza
        print(f"esta en el repositorio{self.cabeza.nombre}")

    def descargarRepositorios(self):
        if os.path.exists(self.datos):
            with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["Repositorios"]:
                repositorio=Repositorio(r["nombre"])
                self.agregar_repositorio(repositorio)

    def agregar_repositorio(self,r,caraga=None):
        if caraga !=None:
            self.cargar_repositorio(r)
        if not self.cabeza:
            self.cabeza = r
        else:
            actual = self.cabeza
            while actual.Repositorio_siguiente:
                actual = actual.Repositorio_siguiente
            actual.Repositorio_siguiente = r
    
    def cargar_repositorio(self,repositorio):

        with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)

        nuevo_repositorio={
            "nombre": repositorio.nombre,
        }
        datos["Repositorios"].append(nuevo_repositorio)     
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    def git_init(self):
        repositorio=Repositorio(input("ingrese el nombre del repositorio"))
        self.agregar_repositorio(repositorio,"Nuevo")

    def repositorios(self):
        actual = self.cabeza
        while actual:
            print("Nombre:", actual.nombre)
            actual = actual.Repositorio_siguiente

    def cambiarRepositorio(self,nombre):
        actual = self.cabeza
        cambio=0
        while actual:
            if actual.nombre==nombre:
                self.repositoriosActual=actual
                cambio=1
                break
            else:
                actual = actual.Repositorio_siguiente
        if cambio==0:
            print("Repositorio no encontrado")