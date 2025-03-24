from modulo1 import *
from modulo2 import *
class Menu:
    def __init__(self):
        self.menu()
    def menu(self):
        bandera =1
        menu1=1
        gestorVersiones=Versiones()
        ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal,gestorVersiones.repositoriosActual.nombre)
        while bandera != 0:
            print()
            if menu1!=0:
                print("gestor de Repositorios")
                print("1) crear repositorio(git init)")
                print("2) cambiar de repocitorio")
                print("3)Repositorios existentes")
                menu1 = int(input("ingrese su elecion: "))
                print()
                if menu1==1:
                    gestorVersiones.git_init()
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal,gestorVersiones.repositoriosActual.nombre)
                elif menu1==2:
                    gestorVersiones.repositorios()
                    gestorVersiones.cambiarRepositorio(input("ingrese el nombre del Repositorio al que desea cambiar"))
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_Principal,gestorVersiones.repositoriosActual.nombre)
                elif menu1==3:
                    gestorVersiones.repositorios()
            else:
                print("1) crear rama(git branch)")
                print("2) cambiar rama(git checkout)")
                print("3) lista de ramas")
                print("4)hacer git add")
                print("5)hacer un commit(git commit -m)")
                print("6)commits realizados(git log)")
                print("7)git merge")
                print("8)git status")
                print("9)regresar al gestor de repositorios")
                bandera = int(input("ingrese su elecion"))
                print()
                if bandera==1:
                    gestorVersiones.repositoriosActual.crear_rama(input("ingrese el nombre: "))
                elif bandera==2:
                    gestorVersiones.repositoriosActual.mostrarRamas()
                    gestorVersiones.repositoriosActual.cambiarRama(input("ingrese el nombre de la rama"))
                    ls = lista_commit(gestorVersiones.repositoriosActual.rama_actual,gestorVersiones.repositoriosActual.nombre)
                elif bandera==3:
                    gestorVersiones.repositoriosActual.mostrarRamas()
                elif bandera==4:
                    ls.git_add(input("ingrese el nombre del archivo"),int(input("ingrese el peso")))
                elif bandera==5:
                    ls.git_commit()
                elif bandera==6:
                    ls.git_log()
                elif bandera==7:
                    ls.git_merge(input("ingrese el nombre"),gestorVersiones.repositoriosActual.nombre)
                elif bandera==8:
                    ls.git_status(gestorVersiones.repositoriosActual.rama_actual,gestorVersiones.repositoriosActual.nombre)
                elif bandera==9:
                    menu1=1
                

                
                
Menu()