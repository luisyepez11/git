import hashlib

class Archivo:
    def __init__(self, nombre, ubicacion, estado, checksum):
        self.nombre = nombre
        self.ubicacion = ubicacion  # Siempre es raíz
        self.estado = estado  # 'A' para Añadido, 'M' para Modificado, 'D' para Eliminado
        self.checksum = checksum

class Staging:
    def __init__(self):
        self.pila = []  # Lista para almacenar archivos en el área de staging
        self.ultimo_commit = None 

    def agregar_archivo(self, nombre, estado):
        ubicacion = "/" + nombre  # Ubicación en la raíz
        checksum = self.calcular_checksum(ubicacion)  # Calcular checksum del archivo
        if checksum:  # Solo agregar si el checksum se calculó exitosamente
            archivo = Archivo(nombre, ubicacion, estado, checksum)
            self.pila.append(archivo)
            print(f"Archivo añadido: {nombre} ({estado})")
        else:
            print(f"No se pudo añadir el archivo: {nombre}")

    def calcular_checksum(self, ubicacion):
        hasher = hashlib.sha1()
        try:
            with open(ubicacion, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except FileNotFoundError:
            print(f"Error: El archivo {ubicacion} no se encontró.")
            return None

    def confirmar_cambios(self):
        print("Cambios confirmados. Archivos en staging:")
        for archivo in self.pila:
            print(f"Confirmado: {archivo.nombre} ({archivo.estado})")
        self.pila.clear()  # Limpiar el área de staging después de confirmar

    def mostrar_archivos(self):
        if not self.pila:
            print("No hay archivos en el área de staging.")
            return
        for archivo in self.pila:
            print(f"{archivo.estado} - {archivo.nombre} ({archivo.ubicacion})")
