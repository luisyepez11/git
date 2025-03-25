import hashlib

class Archivo:
    def __init__(self, nombre, ubicacion, estado, checksum):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.estado = estado  # 'A' for add, 'M' for modify, 'D' for delete
        self.checksum = checksum

class Staging:
    def __init__(self):
        self.pila = []  # List para almacenar archivos en el staging
        self.ultimo_commit = None 

    def agregar_archivo(self, nombre, ubicacion, estado):
        checksum = self.calcular_checksum(ubicacion)
        archivo = Archivo(nombre, ubicacion, estado, checksum)
        self.pila.append(archivo)

    def calcular_checksum(self, ubicacion):
        hasher = hashlib.sha1()
        with open(ubicacion, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def confirmar_cambios(self):
        print("Cambios confirmados. Archivos en staging:")
        for archivo in self.pila:
            print(f"Confirmado: {archivo.nombre} ({archivo.estado})")
        self.pila.clear()  # clean in the staging area after commit

    def mostrar_archivos(self):
        if not self.pila:
            print("No hay archivos en el área de staging.")
            return
        for archivo in self.pila:
            print(f"{archivo.estado} - {archivo.nombre} ({archivo.ubicacion})")
