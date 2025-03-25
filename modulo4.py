from datetime import datetime

class PullRequest:
    def __init__(self, id_pr, titulo, descripcion, autor, rama_origen, rama_destino):
        self.id_pr = id_pr
        self.titulo = titulo
        self.descripcion = descripcion
        self.autor = autor
        self.fecha_creacion = datetime.now()
        self.rama_origen = rama_origen
        self.rama_destino = rama_destino
        self.estado = "pendiente"  # estados: pendiente, en revision, aprobado, fusionado, rechazado
        self.commits_asociados = []
        self.archivos_modificados = []
        self.revisores_asignados = []
        self.fecha_cierre = None

class ColaPullRequests:
    def __init__(self):
        self.cola = []  # lis for storing pull requests

    def crear_pull_request(self, titulo, descripcion, autor, rama_origen, rama_destino):
        id_pr = len(self.cola) + 1  # Generar ID único
        pr = PullRequest(id_pr, titulo, descripcion, autor, rama_origen, rama_destino)
        self.cola.append(pr)
        print(f"Pull Request creado: {pr.id_pr} - {pr.titulo}")

    def mostrar_estado(self):
        if not self.cola:
            print("No hay pull requests en la cola.")
            return
        for pr in self.cola:
            print(f"{pr.id_pr}: {pr.titulo} - {pr.estado}")

    def revisar_pr(self, id_pr):
        for pr in self.cola:
            if pr.id_pr == id_pr:
                pr.estado = "en revisión"
                print(f"Pull Request {id_pr} marcado como en revisión.")
                return
        print(f"Pull Request {id_pr} no encontrado.")

    def aprobar_pr(self, id_pr):
        for pr in self.cola:
            if pr.id_pr == id_pr:
                pr.estado = "aprobado"
                print(f"Pull Request {id_pr} aprobado.")
                return
        print(f"Pull Request {id_pr} no encontrado.")

    def rechazar_pr(self, id_pr):
        for pr in self.cola:
            if pr.id_pr == id_pr:
                pr.estado = "rechazado"
                print(f"Pull Request {id_pr} rechazado.")
                self.cola.remove(pr)
                return
        print(f"Pull Request {id_pr} no encontrado.")

    def cancelar_pr(self, id_pr):
        for pr in self.cola:
            if pr.id_pr == id_pr:
                self.cola.remove(pr)
                print(f"Pull Request {id_pr} cancelado.")
                return
        print(f"Pull Request {id_pr} no encontrado.")

    def listar_pr(self):
        self.mostrar_estado()

    def procesar_siguiente(self):
        if self.cola:
            siguiente_pr = self.cola[0]
            siguiente_pr.estado = "en proceso"
            print(f"Procesando Pull Request: {siguiente_pr.id_pr} - {siguiente_pr.titulo}")
        else:
            print("No hay pull requests para procesar.")
