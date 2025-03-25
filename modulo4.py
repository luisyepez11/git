from datetime import datetime  # Importar módulo para el control de fechas

class PullRequest:  # Clase para manejar los pull requests
    def __init__(self, id_pr, titulo, descripcion, autor, rama_origen, rama_destino):
        self.id_pr = id_pr  # ID de pull request
        self.titulo = titulo  # Título del pull request
        self.descripcion = descripcion  # Descripción del pull request
        self.autor = autor  # Autor del pull request
        self.fecha_creacion = datetime.now()  # Fecha de creación del pull request
        self.rama_origen = rama_origen  # Rama de la ruta de origen
        self.rama_destino = rama_destino  # Rama de destino del pull request
        self.estado = "pendiente"  # Estados: pendiente, en revisión, aprobado, fusionado, rechazado
        self.commits_asociados = []  # Lista de commits asociados al pull request
        self.archivos_modificados = []  # Lista de archivos modificados en el pull request
        self.revisores_asignados = []  # Lista de revisores asignados al pull request
        self.fecha_cierre = None  # Fecha de cierre del pull request (inicialmente None)

class ColaPullRequests:
    def __init__(self):
        self.cola = []  # Lista para almacenar los pull requests

    def crear_pull_request(self, titulo, descripcion, autor, rama_origen, rama_destino):
        id_pr = len(self.cola) + 1  # Generar ID único basado en la longitud de la cola
        pr = PullRequest(id_pr, titulo, descripcion, autor, rama_origen, rama_destino)  # Instanciar el pull request
        self.cola.append(pr)  # Agregar el pull request a la cola
        print(f"Pull Request creado: {pr.id_pr} - {pr.titulo}")  # Mensaje de confirmación

    def mostrar_estado(self):
        if not self.cola:  # Verificar si la cola está vacía
            print("No hay pull requests en la cola.")  # Mensaje si no hay PRs
            return
        for pr in self.cola:  # Iterar sobre los pull requests en la cola
            print(f"{pr.id_pr}: {pr.titulo} - {pr.estado}")  # Mostrar ID, título y estado de cada PR

    def revisar_pr(self, id_pr):
        for pr in self.cola:  # Buscar el pull request por ID
            if pr.id_pr == id_pr:
                pr.estado = "en revisión"  # Cambiar estado a "en revisión"
                print(f"Pull Request {id_pr} marcado como en revisión.")  # Mensaje de confirmación
                return
        print(f"Pull Request {id_pr} no encontrado.")  # Mensaje si no se encuentra el PR

    def aprobar_pr(self, id_pr):
        for pr in self.cola:  # Buscar el pull request por ID
            if pr.id_pr == id_pr:
                pr.estado = "aprobado"  # Cambiar estado a "aprobado"
                print(f"Pull Request {id_pr} aprobado.")  # Mensaje de confirmación
                return
        print(f"Pull Request {id_pr} no encontrado.")  # Mensaje si no se encuentra el PR

    def rechazar_pr(self, id_pr):
        for pr in self.cola:  # Buscar el pull request por ID
            if pr.id_pr == id_pr:
                pr.estado = "rechazado"  # Cambiar estado a "rechazado"
                print(f"Pull Request {id_pr} rechazado.")  # Mensaje de confirmación
                self.cola.remove(pr)  # Eliminar el PR de la cola
                return
        print(f"Pull Request {id_pr} no encontrado.")  # Mensaje si no se encuentra el PR

    def cancelar_pr(self, id_pr):
        for pr in self.cola:  # Buscar el pull request por ID
            if pr.id_pr == id_pr:
                self.cola.remove(pr)  # Eliminar el PR de la cola
                print(f"Pull Request {id_pr} cancelado.")  # Mensaje de confirmación
                return
        print(f"Pull Request {id_pr} no encontrado.")  # Mensaje si no se encuentra el PR

    def listar_pr(self):
        self.mostrar_estado()  # Llamar a mostrar_estado para listar los PRs

    def procesar_siguiente(self):
        if self.cola:  # Verificar si hay pull requests en la cola
            siguiente_pr = self.cola[0]  # Tomar el siguiente PR en la cola
            siguiente_pr.estado = "en proceso"  # Cambiar estado a "en proceso"
            print(f"Procesando Pull Request: {siguiente_pr.id_pr} - {siguiente_pr.titulo}")  # Mensaje de confirmación
        else:
            print("No hay pull requests para procesar.")  # Mensaje si no hay PRs en la cola
