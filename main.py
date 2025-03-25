from modulo1 import *
from modulo2 import *
from modulo3 import Staging
from modulo4 import ColaPullRequests

class Menu:
    def __init__(self):
        self.menu()

    def menu(self):
        bandera = 1
        menu1 = 1
        gestorVersiones = Versiones()
        staging = Staging()
        cola_pr = ColaPullRequests()
        ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, gestorVersiones.repositoriosActual.nombre)
        
        while bandera != 0:
            print()
            if menu1 != 0:
                print("Gestor de Repositorios")
                print("1) Crear repositorio (git init)")
                print("2) Cambiar de repositorio")
                print("3) Repositorios existentes")
                print("4) Área de Staging")
                print("5) Pull Requests")
                menu1 = int(input("Ingrese su elección: "))
                print()
                if menu1 == 1:
                    gestorVersiones.git_init()
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, gestorVersiones.repositoriosActual.nombre)
                elif menu1 == 2:
                    gestorVersiones.repositorios()
                    gestorVersiones.cambiarRepositorio(input("Ingrese el nombre del Repositorio al que desea cambiar: "))
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, gestorVersiones.repositoriosActual.nombre)
                elif menu1 == 3:
                    gestorVersiones.repositorios()
            else:
                print("1) Crear rama (git branch)")
                print("2) Cambiar rama (git checkout)")
                print("3) Lista de ramas")
                print("4) Hacer git add")
                print("5) Hacer un commit (git commit -m)")
                print("6) Commits realizados (git log)")
                print("7) Git merge")
                print("8) Git status")
                print("9) Regresar al gestor de repositorios")
                bandera = int(input("Ingrese su elección: "))
                print()
                if bandera == 1:
                    gestorVersiones.repositoriosActual.crear_rama(input("Ingrese el nombre: "))
                elif bandera == 2:
                    gestorVersiones.repositoriosActual.mostrarRamas()
                    gestorVersiones.repositoriosActual.cambiarRama(input("Ingrese el nombre de la rama: "))
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_actual, gestorVersiones.repositoriosActual.nombre)
                elif bandera == 3:
                    gestorVersiones.repositoriosActual.mostrarRamas()
                elif bandera == 4:
                    nombre_archivo = input("Ingrese el nombre del archivo: ")
                    ubicacion_archivo = input("Ingrese la ubicación del archivo: ")
                    estado = input("Ingrese el estado (A/M/D): ")
                    staging.agregar_archivo(nombre_archivo, ubicacion_archivo, estado)
                elif bandera == 5:
                    staging.confirmar_cambios()
                    ls.git_commit(input("Ingrese el mensaje del commit: "), gestorVersiones.repositoriosActual.rama_actual, gestorVersiones.repositoriosActual.nombre)
                elif bandera == 6:
                    ls.git_log()
                elif bandera == 7:
                    ls.git_merge(input("Ingrese el nombre: "), gestorVersiones.repositoriosActual.nombre)
                elif bandera == 8:
                    ls.git_status(gestorVersiones.repositoriosActual.rama_actual, gestorVersiones.repositoriosActual.nombre)
                elif bandera == 9:
                    menu1 = 1

            # Menu del pull request
            if menu1 == 5:
                print("1) Crear Pull Request")
                print("2) Mostrar estado de Pull Requests")
                print("3) Revisar Pull Request")
                print("4) Aprobar Pull Request")
                print("5) Rechazar Pull Request")
                print("6) Cancelar Pull Request")
                print("7) Listar Pull Requests")
                print("8) Procesar siguiente Pull Request")
                submenu = int(input("Ingrese su elección: "))
                if submenu == 1:
                    titulo = input("Ingrese el título: ")
                    descripcion = input("Ingrese la descripción: ")
                    autor = input("Ingrese su nombre: ")
                    rama_origen = input("Ingrese la rama de origen: ")
                    rama_destino = input("Ingrese la rama de destino: ")
                    cola_pr.crear_pull_request(titulo, descripcion, autor, rama_origen, rama_destino)
                elif submenu == 2:
                    cola_pr.mostrar_estado()
                elif submenu == 3:
                    id_pr = int(input("Ingrese el ID del Pull Request a revisar: "))
                    cola_pr.revisar_pr(id_pr)
                elif submenu == 4:
                    id_pr = int(input("Ingrese el ID del Pull Request a aprobar: "))
                    cola_pr.aprobar_pr(id_pr)
                elif submenu == 5:
                    id_pr = int(input("Ingrese el ID del Pull Request a rechazar: "))
                    cola_pr.rechazar_pr(id_pr)
                elif submenu == 6:
                    id_pr = int(input("Ingrese el ID del Pull Request a cancelar: "))
                    cola_pr.cancelar_pr(id_pr)
                elif submenu == 7:
                    cola_pr.listar_pr()
                elif submenu == 8:
                    cola_pr.procesar_siguiente()

Menu()
