import hashlib  # Modulo para calcular checksums

class Archivo:
    def __init__(self, nombre, ubicacion, estado, checksum):
        # Iniciamos un objeto Archivo con los siguientes atributos
        self.nombre = nombre
        self.ubicacion = ubicacion # la ubicacion es la raiz del sistema de archivos
        self.estado = estado  # Estado del archivo ('A' para Agregado, 'M' para Modificado, 'D' para Eliminado)
        self.checksum = checksum  # Checksum del archivo para verificar integridad
        # el checksum es un valor unico que se calcula a partir del contenido del archivo

class Staging:
    def __init__(self):
        # inicciamos el area de staging con una pila vacia y sin commit
        self.pila = []  # en esta pila se almacenan los archivos que se agregan al area de staging
        self.ultimo_commit = None  # esto almacenara el ultimo commit realizado

    def agregar_archivo(self, nombre, estado): 
        # metodo add que es para agregar un archivo al area de staging
        ubicacion = nombre  # aqui defino la ubicaicon que es la raiz
        checksum = self.calcular_checksum(ubicacion)  # Calcula el checksum del archivo 
        if checksum:  # Solo agrega el archivo si el checksum se caluclo bien
            archivo = Archivo(nombre, ubicacion, estado, checksum)  # Crea un objeto Archivo
            self.pila.append(archivo)  # Agrega el archivo a la pila de staging
            print(f"Archivo agregado: {nombre} ({estado})") 
        else:
            print(f"No se pudo agregar el archivo: {nombre}")

    def calcular_checksum(self, ubicacion):
        hasher = hashlib.sha1()  # Crea un objeto hash utilizando SHA-1
        try:
            with open(ubicacion, 'rb') as f:  # Intenta abrir el archivo en modo binario
                while chunk := f.read(8192):  # Lee el archivo en bloques de 8192 bytes porqe es mas eficiente
                    hasher.update(chunk)  # actualiza el hash con el contenido del archivo
            return hasher.hexdigest()  # Retorna el checksum en formato hexadecimal
        except FileNotFoundError:
            print(f"Error: El archivo {ubicacion} no se encontró.")
            return None  # devuelve None si hay error

    def confirmar_cambios(self):
        print("Cambios confirmados. Archivos en staging:")
        for archivo in self.pila:  # Itera sobre los archivos en la pila de staging
            print(f"Confirmado: {archivo.nombre} ({archivo.estado})")
        self.pila.clear() # limpiamos el area de staging

    def mostrar_archivos(self):

        if not self.pila:  #  vemos si al pila no tiene nada
            print("No hay archivos en el área de staging.") 
            return
        for archivo in self.pila:  # nteramos en los archivos en la pila de staging
            print(f"{archivo.estado} - {archivo.nombre} ({archivo.ubicacion})")
