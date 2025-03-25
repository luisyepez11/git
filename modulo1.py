# Importar módulos necesarios
import json
import os

# Clase que representa un repositorio de control de versiones
class Repositorio:
    def __init__(self, nombre):
        # Inicializar propiedades del repositorio
        self.nombre = nombre
        self.ramas = []  # Lista para almacenar ramas
        self.commit_resiente = None  # Último commit realizado
        self.rama_actual = "main"  # Rama actual por defecto
        self.rama_Principal = "main"  # Rama principal
        self.ramasDatos = f"{nombre}.json"  # Archivo para datos de ramas
        self.Repositorio_siguiente = None  # Siguiente repositorio en lista
        self.descargar_ramas()  # Cargar ramas existentes

    # Método para crear nueva rama
    def crear_rama(self, nombre):
        # Validar nombre no vacío
        if nombre == "":
            print("No ingresó ningún nombre")
        else:
            # Verificar si rama ya existe
            bandera = 0
            for i in self.ramas:
                if nombre == i:
                    print("Ya hay una rama llamada así")
                    bandera = 1
            
            # Si no existe, crear nueva rama
            if bandera == 0:   
                rama = Rama(nombre, self.nombre)
                self.ramas.append(rama)
                self.cargar_ramas(rama)
                
                # Copiar commits de rama actual a nueva rama
                datos_commit = f"{self.nombre}_{self.rama_actual}_commit.json"
                with open(datos_commit, 'r') as archivo:
                    datos = json.load(archivo)
                
                datos_commit = f"{self.nombre}_{rama.nombre}_commit.json"
                with open(datos_commit, 'w') as archivo:
                    json.dump(datos, archivo, indent=4)
                
                print(f"\nSe creó una nueva rama {nombre}")
    
    # Método para cargar ramas desde archivo
    def descargar_ramas(self):
        if os.path.exists(self.ramasDatos):
            with open(self.ramasDatos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["rama"]:
                rama_cargada = Rama(r['nombre'], self.nombre)
                self.ramas.append(rama_cargada)
            print("Descarga exitosa")
        else:
            # Crear archivo con rama main si no existe
            commit = f"{self.nombre}_main_commit.js"
            datos = {"rama": []}
            rama = {
                "nombre": "main",
                "commit": commit,
            }
            datos["rama"].append(rama)
            with open(self.ramasDatos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
        
    # Método para guardar rama en archivo
    def cargar_ramas(self, rama):
        with open(self.ramasDatos, 'r') as archivo:
            datos = json.load(archivo)
        
        nueva_rama = {
            "nombre": rama.nombre,
            "commit": rama.commit,
        }
        datos["rama"].append(nueva_rama)
        
        with open(self.ramasDatos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
    # Método para mostrar todas las ramas
    def mostrarRamas(self):
        for i in self.ramas:
            print(i.nombre)
            
    # Método para cambiar rama actual
    def cambiarRama(self, nombre):
        cambio = 0
        for i in self.ramas:
            if i.nombre == nombre:
                self.rama_actual = i.nombre
                cambio = 1
        if cambio == 0:
            print("No existe esa rama")

# Clase que representa una rama del repositorio
class Rama:
    def __init__(self, nombre, nombreRepositorio):
        self.nombre = nombre  # Nombre de la rama
        self.commit = f"{nombreRepositorio}_{nombre}_commit.js"  # Archivo de commits

# Clase principal que gestiona múltiples repositorios
class Versiones:
    def __init__(self):
        self.cabeza = None  # Primer repositorio
        self.datos = "DatosRepositorios.json"  # Archivo de repositorios
        
        # Crear archivo si no existe
        if not os.path.exists(self.datos):
            datos = {"Repositorios": []}
            with open(self.datos, 'w') as archivo:
                json.dump(datos, archivo, indent=4)
            print("ingrese el nombre del repositorio inicial")
            self.git_init()      
        
        self.descargarRepositorios()  # Cargar repositorios
        self.repositoriosActual = self.cabeza  # Repositorio actual
        print(f"esta en el repositorio{self.cabeza.nombre}")

    # Método para cargar repositorios desde archivo
    def descargarRepositorios(self):
        if os.path.exists(self.datos):
            with open(self.datos, 'r') as archivo:
                datos = json.load(archivo)
            for r in datos["Repositorios"]:
                repositorio = Repositorio(r["nombre"])
                self.agregar_repositorio(repositorio)

    # Método para añadir repositorio a lista
    def agregar_repositorio(self, r, caraga=None):
        if caraga != None:
            self.cargar_repositorio(r)
        
        if not self.cabeza:
            self.cabeza = r  # Primer elemento
        else:
            actual = self.cabeza
            while actual.Repositorio_siguiente:
                actual = actual.Repositorio_siguiente
            actual.Repositorio_siguiente = r  # Añadir al final
    
    # Método para guardar repositorio en archivo
    def cargar_repositorio(self, repositorio):
        with open(self.datos, 'r') as archivo:
            datos = json.load(archivo)

        nuevo_repositorio = {
            "nombre": repositorio.nombre,
        }
        datos["Repositorios"].append(nuevo_repositorio)
        
        with open(self.datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)
    
    # Método para crear nuevo repositorio
    def git_init(self):
        repositorio = Repositorio(input("ingrese el nombre del repositorio"))
        self.agregar_repositorio(repositorio, "Nuevo")

    # Método para listar repositorios
    def repositorios(self):
        actual = self.cabeza
        while actual:
            print("Nombre:", actual.nombre)
            actual = actual.Repositorio_siguiente

    # Método para cambiar repositorio actual
    def cambiarRepositorio(self, nombre):
        actual = self.cabeza
        cambio = 0
        while actual:
            if actual.nombre == nombre:
                self.repositoriosActual = actual
                cambio = 1
                break
            else:
                actual = actual.Repositorio_siguiente
        if cambio == 0:
            print("Repositorio no encontrado")
