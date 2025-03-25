# Importación de módulos necesarios
from modulo1 import *  # Importa todas las funciones/clases de modulo1
from modulo2 import *  # Importa todas las funciones/clases de modulo2
from modulo3 import Staging  # Importa específicamente la clase Staging
from modulo4 import ColaPullRequests  # Importa específicamente la clase ColaPullRequests

class Menu:
    def __init__(self):
        # Constructor que inicia el menú al crear una instancia
        self.menu()

    def menu(self):
        # Inicialización de variables y componentes principales
        bandera = 1  # Controla el bucle principal
        menu1 = 1    # Controla el menú actual (repositorios o ramas)
        
        # Instancias de las clases principales
        gestorVersiones = Versiones()  # Gestiona los repositorios
        staging = Staging()  # Maneja el área de staging
        cola_pr = ColaPullRequests()  # Administra los pull requests
        
        # Inicializa la lista de commits para la rama principal
        ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, 
                         gestorVersiones.repositoriosActual.nombre)

        # Bucle principal del menú
        while bandera != 0:
            print()  # Espacio en blanco para mejor legibilidad

            # Menú de gestión de repositorios (cuando menu1 != 0)
            if menu1 != 0:
                print("Gestor de Repositorios")
                print("1) Crear repositorio (git init)")
                print("2) Cambiar de repositorio")
                print("3) Repositorios existentes")
                print("4) Área de Staging")
                print("5) Pull Requests")
                print("0) Cambiar al menu de Ramas")
                
                menu1 = int(input("Ingrese su elección: "))
                print()  # Espacio en blanco

                # Opciones del menú de repositorios
                if menu1 == 1:
                    gestorVersiones.git_init()  # Crea un nuevo repositorio
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, 
                                    gestorVersiones.repositoriosActual.nombre)
                elif menu1 == 2:
                    gestorVersiones.repositorios()  # Muestra repositorios existentes
                    gestorVersiones.cambiarRepositorio(
                        input("Ingrese el nombre del Repositorio al que desea cambiar: "))
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal, 
                                    gestorVersiones.repositoriosActual.nombre)
                elif menu1 == 3:
                    gestorVersiones.repositorios()  # Lista repositorios existentes

            # Menú de gestión de ramas (cuando menu1 == 0)
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
                print()  # Espacio en blanco

                # Opciones del menú de ramas
                if bandera == 1:
                    gestorVersiones.repositoriosActual.crear_rama(
                        input("Ingrese el nombre: "))  # Crea nueva rama
                elif bandera == 2:
                    gestorVersiones.repositoriosActual.mostrarRamas()  # Muestra ramas
                    gestorVersiones.repositoriosActual.cambiarRama(
                        input("Ingrese el nombre de la rama: "))  # Cambia de rama
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_actual, 
                                    gestorVersiones.repositoriosActual.nombre)
                elif bandera == 3:
                    gestorVersiones.repositoriosActual.mostrarRamas()  # Lista ramas
                elif bandera == 4:
                    # Agrega archivos al staging
                    nombre_archivo = input("Ingrese el nombre del archivo: ")
                    estado = input("Ingrese el estado (A/M/D): ")
                    peso = int(input("Ingrese el peso en megaBytes"))
                    ls.git_add(nombre_archivo, peso)
                    staging.agregar_archivo(nombre_archivo, estado)
                elif bandera == 5:
                    ls.git_commit()  # Realiza commit
                    staging.confirmar_cambios()  # Confirma cambios en staging
                elif bandera == 6:
                    ls.git_log()  # Muestra historial de commits
                elif bandera == 7:
                    ls.git_merge(input("Ingrese el nombre: "),  # Realiza merge
                               gestorVersiones.repositoriosActual.nombre)
                elif bandera == 8:
                    ls.git_status(gestorVersiones.repositoriosActual.rama_actual,  # Muestra estado
                                gestorVersiones.repositoriosActual.nombre)
                elif bandera == 9:
                    menu1 = 1  # Regresa al menú de repositorios

            # Menú de Pull Requests (opción 5 del menú principal)
            if menu1 == 5:
                print("1) Crear Pull Request")
                print("2) Mostrar estado de Pull Requests")
                print("3) Revisar Pull Request")
                print("4) Aprobar Pull Request")
                print("5) Rechazar Pull Request")
                print("6) Cancelar Pull Request")
                print("7) Listar Pull Requests")
                print("8) Procesar siguiente Pull Request")
                print("9) Volver al menu anterior")
                
                submenu = int(input("Ingrese su elección: "))

                # Opciones del menú de Pull Requests
                if submenu == 1:
                    # Crea nuevo Pull Request
                    titulo = input("Ingrese el título: ")
                    descripcion = input("Ingrese la descripción: ")
                    autor = input("Ingrese su nombre: ")
                    rama_origen = input("Ingrese la rama de origen: ")
                    rama_destino = input("Ingrese la rama de destino: ")
                    cola_pr.crear_pull_request(titulo, descripcion, autor, rama_origen, rama_destino)
                elif submenu == 2:
                    cola_pr.mostrar_estado()  # Muestra estado de PRs
                elif submenu == 3:
                    id_pr = int(input("Ingrese el ID del Pull Request a revisar: "))
                    cola_pr.revisar_pr(id_pr)  # Revisa PR específico
                elif submenu == 4:
                    id_pr = int(input("Ingrese el ID del Pull Request a aprobar: "))
                    cola_pr.aprobar_pr(id_pr)  # Aprueba PR
                elif submenu == 5:
                    id_pr = int(input("Ingrese el ID del Pull Request a rechazar: "))
                    cola_pr.rechazar_pr(id_pr)  # Rechaza PR
                elif submenu == 6:
                    id_pr = int(input("Ingrese el ID del Pull Request a cancelar: "))
                    cola_pr.cancelar_pr(id_pr)  # Cancela PR
                elif submenu == 7:
                    cola_pr.listar_pr()  # Lista todos los PRs
                elif submenu == 8:
                    cola_pr.procesar_siguiente()  # Procesa siguiente PR en cola
                elif submenu == 9:
                    menu1 = 1  # Regresa al menú principal

# Inicia la aplicación creando una instancia del Menu
Menu()
