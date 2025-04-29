# ============================
# ESTRUCTURAS PERSONALIZADAS
# ============================

import hashlib
from datetime import datetime

# ----------- Lista Enlazada -----------

class NodoLista:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.primero = None

    def agregar(self, dato):
        nuevo = NodoLista(dato)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def recorrer(self):
        actual = self.primero
        while actual:
            yield actual.dato
            actual = actual.siguiente

    def buscar(self, criterio_func):
        actual = self.primero
        while actual:
            if criterio_func(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

# ----------- Pila -----------

class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.anterior = None

class Pila:
    def __init__(self):
        self.tope = None

    def push(self, dato):
        nuevo = NodoPila(dato)
        nuevo.anterior = self.tope
        self.tope = nuevo

    def pop(self):
        if self.tope:
            dato = self.tope.dato
            self.tope = self.tope.anterior
            return dato
        return None

    def peek(self):
        return self.tope.dato if self.tope else None

    def vacia(self):
        return self.tope is None

    def recorrer(self):
        actual = self.tope
        while actual:
            yield actual.dato
            actual = actual.anterior

# ----------- Cola -----------

class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, dato):
        nuevo = NodoCola(dato)
        if not self.frente:
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def desencolar(self):
        if not self.frente:
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return dato

    def vacia(self):
        return self.frente is None

    def recorrer(self):
        actual = self.frente
        while actual:
            yield actual.dato
            actual = actual.siguiente

# ============================
# CLASES DE NEGOCIO
# ============================

# ----- Archivo -----

class Archivo:
    def __init__(self, nombre, contenido):
        self.nombre = nombre
        self.contenido = contenido
        self.checksum = hashlib.sha1(contenido.encode()).hexdigest()
        self.estado = 'A'  # A: Añadido, M: Modificado, D: Eliminado
        self.metadatos = {'nombre': nombre, 'tamano': len(contenido)}

# ----- Commit -----

class Commit:
    def __init__(self, mensaje, autor, archivos, padre=None):
        self.id = hashlib.sha1((mensaje + str(datetime.now())).encode()).hexdigest()[:8]
        self.mensaje = mensaje
        self.autor = autor
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.archivos = archivos  # ListaEnlazada
        self.padre = padre  # Referencia al commit padre

# ----- Pull Request -----

class PullRequest:
    def __init__(self, id_pr, titulo, descripcion, autor, source_branch, target_branch, commits):
        self.id = id_pr
        self.titulo = titulo
        self.descripcion = descripcion
        self.autor = autor
        self.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.commits = commits  # ListaEnlazada
        self.estado = 'pendiente'
        self.revisores = ListaEnlazada()
        self.etiqueta = ''
        self.fecha_cierre = None

# ----- Rama (Nodo N-ario) -----

class Rama:
    def __init__(self, nombre):
        self.nombre = nombre
        self.commits = ListaEnlazada()
        self.hijos = ListaEnlazada()
        self.padre = None

# ----- Repositorio -----

class Repositorio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.branch_root = Rama('main')
        self.branch_actual = self.branch_root
        self.staging = Pila()
        self.pull_requests = Cola()
        self.colaboradores = None  # Árbol binario a implementar en Parte 4
        self.archivos_btree = None  # B-tree a implementar en Parte 5
        self.roles_avl = None  # AVL a implementar en Parte 6

# ============================
# SISTEMA PRINCIPAL: GitSystem
# ============================

class GitSystem:
    def __init__(self):
        self.repositorios = ListaEnlazada()
        self.repositorio_actual = None

    # ----------- Comandos Básicos -----------

    def git_init(self):
        nombre = input("Nombre del repositorio: ")
        nuevo_repo = Repositorio(nombre)
        self.repositorios.agregar(nuevo_repo)
        self.repositorio_actual = nuevo_repo
        print(f"[git init] Repositorio '{nombre}' creado y seleccionado.")

    def git_add(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        nombre = input("Nombre del archivo: ")
        contenido = input("Contenido del archivo: ")
        archivo = Archivo(nombre, contenido)
        self.repositorio_actual.staging.push(archivo)
        print(f"[git add {nombre}] Añadido al área de staging.")

    def git_status(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        print("[git status] Archivos en staging:")
        for archivo in self.repositorio_actual.staging.recorrer():
            print(f"- {archivo.nombre} ({archivo.estado})")

    def git_commit(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        mensaje = input("Mensaje del commit: ")
        autor = input("Correo del autor: ")
        archivos = ListaEnlazada()
        while not self.repositorio_actual.staging.vacia():
            archivo = self.repositorio_actual.staging.pop()
            archivos.agregar(archivo)
        padre = None
        rama = self.repositorio_actual.branch_actual
        if rama.commits.primero:
            padre = rama.commits.primero.dato
        nuevo_commit = Commit(mensaje, autor, archivos, padre)
        rama.commits.agregar(nuevo_commit)
        print(f"[git commit -m \"{mensaje}\"] Commit {nuevo_commit.id} creado.")

    def git_log(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        print("[git log] Historial de commits:")
        for commit in self.repositorio_actual.branch_actual.commits.recorrer():
            print(f"ID: {commit.id} | Autor: {commit.autor} | Fecha: {commit.fecha} | Mensaje: {commit.mensaje}")

    def git_checkout_commit(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        objetivo = input("ID del commit al que quieres volver: ")
        for commit in self.repositorio_actual.branch_actual.commits.recorrer():
            if commit.id == objetivo:
                print(f"[git checkout {objetivo}] Estado restaurado al commit: {commit.id}")
                return
        print("Commit no encontrado.")

    # ----------- Pull Requests -----------

    def git_pr_create(self):
        if not self.repositorio_actual:
            print("Primero debes crear o seleccionar un repositorio.")
            return
        id_pr = input("ID del PR: ")
        titulo = input("Título: ")
        descripcion = input("Descripción: ")
        autor = input("Autor: ")
        source = input("Rama origen: ")
        target = input("Rama destino: ")
        commits = self.repositorio_actual.branch_actual.commits
        pr = PullRequest(id_pr, titulo, descripcion, autor, source, target, commits)
        self.repositorio_actual.pull_requests.encolar(pr)
        print(f"[git pr create {source} {target}] Pull request '{titulo}' creado.")

    def git_pr_status(self):
        print("[git pr status] Estado de los PRs:")
        for pr in self.repositorio_actual.pull_requests.recorrer():
            print(f"- PR {pr.id}: {pr.estado}")

    def git_pr_approve(self):
        id_pr = input("ID del PR a aprobar: ")
        for pr in self.repositorio_actual.pull_requests.recorrer():
            if pr.id == id_pr:
                pr.estado = 'aprobado'
                pr.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[git pr approve {id_pr}] Pull request aprobado.")
                return
        print("PR no encontrado.")

    def git_pr_list(self):
        print("[git pr list] Lista de PRs:")
        for pr in self.repositorio_actual.pull_requests.recorrer():
            print(f"ID: {pr.id} | Estado: {pr.estado} | Título: {pr.titulo} | Etiqueta: {pr.etiqueta}")

    def git_pr_reject(self):
        id_pr = input("ID del PR a rechazar: ")
        for pr in self.repositorio_actual.pull_requests.recorrer():
            if pr.id == id_pr:
                pr.estado = 'rechazado'
                pr.fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[git pr reject {id_pr}] Rechazado.")
                return
        print("PR no encontrado.")

    def git_pr_cancel(self):
        id_pr = input("ID del PR a cancelar: ")
        nueva_cola = Cola()
        encontrado = False
        while not self.repositorio_actual.pull_requests.vacia():
            pr = self.repositorio_actual.pull_requests.desencolar()
            if pr.id == id_pr:
                encontrado = True
                continue
            nueva_cola.encolar(pr)
        self.repositorio_actual.pull_requests = nueva_cola
        print(f"[git pr cancel {id_pr}] Cancelado." if encontrado else "PR no encontrado.")

    def git_pr_tag(self):
        id_pr = input("ID del PR: ")
        etiqueta = input("Etiqueta: ")
        for pr in self.repositorio_actual.pull_requests.recorrer():
            if pr.id == id_pr:
                pr.etiqueta = etiqueta
                print(f"[git pr tag {id_pr} {etiqueta}] Etiqueta asignada.")
                return
        print("PR no encontrado.")

    def git_pr_clear(self):
        self.repositorio_actual.pull_requests = Cola()
        print("[git pr clear] Todos los PRs eliminados.")

    def git_pr_next(self):
        pr = self.repositorio_actual.pull_requests.desencolar()
        if pr:
            pr.estado = 'en proceso'
            print(f"[git pr next] Procesando PR {pr.id}")
        else:
            print("No hay PRs pendientes.")

# ============================
# COMANDOS DE RAMAS (Árbol N-ario)
# ============================

    def git_branch_create(self):
        nombre = input("Nombre de la nueva rama: ")
        nueva_rama = Rama(nombre)
        nueva_rama.padre = self.repositorio_actual.branch_actual
        self.repositorio_actual.branch_actual.hijos.agregar(nueva_rama)
        print(f"[git branch {nombre}] Rama creada desde '{self.repositorio_actual.branch_actual.nombre}'.")

    def git_branch_list(self):
        print("[git branch --list] Árbol de ramas:")
        self._mostrar_ramas_preorden(self.repositorio_actual.branch_root, 0)

    def _mostrar_ramas_preorden(self, rama, nivel):
        print("  " * nivel + f"- {rama.nombre}")
        for hijo in rama.hijos.recorrer():
            self._mostrar_ramas_preorden(hijo, nivel + 1)

    def git_branch_delete(self):
        nombre = input("Nombre de la rama a eliminar: ")
        if nombre == 'main':
            print("No se puede eliminar la rama 'main'.")
            return
        padre = self.repositorio_actual.branch_actual
        nueva_lista = ListaEnlazada()
        eliminado = False
        for hijo in padre.hijos.recorrer():
            if hijo.nombre == nombre:
                eliminado = True
                continue
            nueva_lista.agregar(hijo)
        padre.hijos = nueva_lista
        print(f"[git branch -d {nombre}] Rama eliminada." if eliminado else "Rama no encontrada.")

    def git_checkout_branch(self):
        nombre = input("Nombre de la rama a cambiar: ")
        rama = self._buscar_rama(self.repositorio_actual.branch_root, nombre)
        if rama:
            self.repositorio_actual.branch_actual = rama
            print(f"[git checkout {nombre}] Cambiado a la rama '{nombre}'.")
        else:
            print("Rama no encontrada.")

    def _buscar_rama(self, rama, nombre):
        if rama.nombre == nombre:
            return rama
        for hijo in rama.hijos.recorrer():
            resultado = self._buscar_rama(hijo, nombre)
            if resultado:
                return resultado
        return None

    def git_merge(self):
        origen = input("Rama origen: ")
        destino = input("Rama destino: ")
        rama_origen = self._buscar_rama(self.repositorio_actual.branch_root, origen)
        rama_destino = self._buscar_rama(self.repositorio_actual.branch_root, destino)

        if not rama_origen or not rama_destino:
            print("Una de las ramas no existe.")
            return

        for commit in rama_origen.commits.recorrer():
            rama_destino.commits.agregar(commit)

        nuevo_commit = Commit(
            mensaje=f"Merge de {origen} en {destino}",
            autor="sistema@merge.git",
            archivos=ListaEnlazada(),
            padre=None
        )
        rama_destino.commits.agregar(nuevo_commit)
        print(f"[git merge {origen} {destino}] Ramas fusionadas.")
    def git_add_contributor(self):
        nombre = input("Nombre del colaborador: ")
        autor = input("Email: ")
        rol = input("Rol: ")
        if not self.repositorio_actual.colaboradores:
            self.repositorio_actual.colaboradores = ABBColaboradores()
        self.repositorio_actual.colaboradores.insertar(nombre, autor, rol)
        print(f"[git add-contributor {nombre}] Colaborador agregado.")

    def git_remove_contributor(self):
        nombre = input("Nombre del colaborador a eliminar: ")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        eliminado = self.repositorio_actual.colaboradores.eliminar(nombre)
        if eliminado:
            print(f"[git remove-contributor {nombre}] Eliminado.")
        else:
            print("Colaborador no encontrado.")

    def git_find_contributor(self):
        nombre = input("Nombre a buscar: ")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        nodo = self.repositorio_actual.colaboradores.buscar(nombre)
        if nodo:
            print(f"[git find-contributor {nombre}] Encontrado: {nodo.autor}, rol: {nodo.rol}")
        else:
            print("No encontrado.")

    def git_contributors(self):
        print("[git contributors] Lista de colaboradores:")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        for nodo in self.repositorio_actual.colaboradores.preorden():
            print(f"- {nodo.nombre} ({nodo.rol}) <{nodo.autor}>")
    def git_file_add(self):
        nombre = input("Nombre del archivo: ")
        contenido = input("Contenido: ")
        archivo = Archivo(nombre, contenido)
        sha = archivo.checksum
        if not self.repositorio_actual.archivos_btree:
            self.repositorio_actual.archivos_btree = BTreeArchivos()
        self.repositorio_actual.archivos_btree.insertar(sha, archivo)
        print(f"[git file-add] Archivo '{nombre}' agregado con SHA {sha}.")

    def git_file_find(self):
        sha = input("SHA-1 del archivo a buscar: ")
        if not self.repositorio_actual.archivos_btree:
            print("No hay archivos.")
            return
        archivo = self.repositorio_actual.archivos_btree.buscar(sha)
        if archivo:
            print(f"Archivo encontrado: {archivo.nombre} | Contenido: {archivo.contenido}")
        else:
            print("Archivo no encontrado.")

    def git_file_list(self):
        print("[git file-list] Archivos almacenados (preorden):")
        if not self.repositorio_actual.archivos_btree:
            print("No hay archivos.")
            return
        self.repositorio_actual.archivos_btree.preorden()
    def git_role_add(self):
        email = input("Email: ")
        rol_nombre = input("Rol: ")
        permisos = input("Permisos (separados por coma): ").split(",")

        if not self.repositorio_actual.roles_avl:
            self.repositorio_actual.roles_avl = ListaRoles()

        self.repositorio_actual.roles_avl.agregar_rol(rol_nombre)
        rol = self.repositorio_actual.roles_avl.get_rol(rol_nombre)

        permisos_lista = ListaEnlazada()
        for p in permisos:
            permisos_lista.agregar(p.strip())

        rol.permisos_tree.insertar(email, permisos_lista)
        print(f"[git role add {email} {rol_nombre} ...] Permisos asignados.")

    def git_role_update(self):
        email = input("Email: ")
        nuevo_rol = input("Nuevo rol: ")
        nuevos_permisos = input("Nuevos permisos (coma): ").split(",")

        self.git_role_remove(email)
        permisos_lista = ListaEnlazada()
        for p in nuevos_permisos:
            permisos_lista.agregar(p.strip())
        self.repositorio_actual.roles_avl.agregar_rol(nuevo_rol)
        rol = self.repositorio_actual.roles_avl.get_rol(nuevo_rol)
        rol.permisos_tree.insertar(email, permisos_lista)
        print(f"[git role update {email} {nuevo_rol} ...] Rol actualizado.")

    def git_role_remove(self, email=None):
        if email is None:
            email = input("Email: ")

        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            if rol.permisos_tree.buscar(email):
                rol.permisos_tree.raiz = self._eliminar_de_avl(rol.permisos_tree.raiz, email)
                print(f"[git role remove {email}] Eliminado.")
                return
        print("Email no encontrado.")

    def _eliminar_de_avl(self, nodo, email):
        if not nodo:
            return nodo
        if email < nodo.email:
            nodo.izq = self._eliminar_de_avl(nodo.izq, email)
        elif email > nodo.email:
            nodo.der = self._eliminar_de_avl(nodo.der, email)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            temp = nodo.der
            while temp.izq:
                temp = temp.izq
            nodo.email, nodo.permisos = temp.email, temp.permisos
            nodo.der = self._eliminar_de_avl(nodo.der, temp.email)
        return nodo

    def git_role_show(self):
        email = input("Email: ")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            nodo = rol.permisos_tree.buscar(email)
            if nodo:
                print(f"Rol: {rol.nombre}")
                print("Permisos:", ", ".join(p for p in nodo.permisos.recorrer()))
                return
        print("Usuario no encontrado.")

    def git_role_check(self):
        email = input("Email: ")
        accion = input("Acción: ")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            nodo = rol.permisos_tree.buscar(email)
            if nodo:
                if any(p == accion for p in nodo.permisos.recorrer()):
                    print(f"[git role check {email} {accion}] ✅ Permitido")
                    return
        print(f"[git role check {email} {accion}] ❌ Denegado")

    def git_role_list(self):
        print("[git role list] Colaboradores con sus permisos (postorden):")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            print(f"Rol: {rol.nombre}")
            rol.permisos_tree.postorden()
    def ejecutar(self):
        comandos = {
            "1": self.git_init,
            "2": self.git_add,
            "3": self.git_commit,
            "4": self.git_status,
            "5": self.git_log,
            "6": self.git_checkout_commit,
            "7": self.git_branch_create,
            "8": self.git_branch_delete,
            "9": self.git_branch_list,
            "10": self.git_checkout_branch,
            "11": self.git_merge,
            "12": self.git_pr_create,
            "13": self.git_pr_status,
            "15": self.git_pr_approve,
            "16": self.git_pr_reject,
            "17": self.git_pr_cancel,
            "18": self.git_pr_list,
            "19": self.git_pr_next,
            "20": self.git_pr_tag,
            "21": self.git_pr_clear,
            "22": self.git_add_contributor,
            "23": self.git_remove_contributor,
            "24": self.git_find_contributor,
            "25": self.git_contributors,
            "26": self.git_file_add,
            "27": self.git_file_find,
            "28": self.git_file_list,
            "29": self.git_role_add,
            "30": self.git_role_update,
            "31": self.git_role_remove,
            "32": self.git_role_show,
            "33": self.git_role_check,
            "34": self.git_role_list
        }

        while True:
            print("\n==== MENÚ GIT SIMULADO (completo) ====")
            print("1. git init")
            print("2. git add")
            print("3. git commit")
            print("4. git status")
            print("5. git log")
            print("6. git checkout <commit_id>")
            print("7. git branch <nombre>")
            print("8. git branch -d <nombre>")
            print("9. git branch --list")
            print("10. git checkout <rama>")
            print("11. git merge <origen> <destino>")
            print("12. git pr create")
            print("13. git pr status")
            print("14. git pr review")
            print("15. git pr approve")
            print("16. git pr reject")
            print("17. git pr cancel")
            print("18. git pr list")
            print("19. git pr next")
            print("20. git pr tag")
            print("21. git pr clear")
            print("22. git add-contributor")
            print("23. git remove-contributor")
            print("24. git find-contributor")
            print("25. git contributors")
            print("26. git file-add")
            print("27. git file-find")
            print("28. git file-list")
            print("29. git role add")
            print("30. git role update")
            print("31. git role remove")
            print("32. git role show")
            print("33. git role check")
            print("34. git role list")
            print("0. Salir")
            
            op = input("Selecciona una opción: ")

            if op == "0":
                break
            
            comando = comandos.get(op)
            if comando:
                comando()
            else:
                print("Comando no válido.")




# ============================
# ÁRBOL BINARIO DE BÚSQUEDA PARA COLABORADORES
# ============================

class NodoABB:
    def __init__(self, nombre, autor, rol):
        self.nombre = nombre
        self.autor = autor
        self.rol = rol
        self.izquierda = None
        self.derecha = None

class ABBColaboradores:
    def __init__(self):
        self.raiz = None

    def insertar(self, nombre, autor, rol):
        self.raiz = self._insertar(self.raiz, nombre, autor, rol)

    def _insertar(self, nodo, nombre, autor, rol):
        if nodo is None:
            return NodoABB(nombre, autor, rol)
        if nombre < nodo.nombre:
            nodo.izquierda = self._insertar(nodo.izquierda, nombre, autor, rol)
        else:
            nodo.derecha = self._insertar(nodo.derecha, nombre, autor, rol)
        return nodo

    def inorden(self):
        yield from self._inorden(self.raiz)

    def _inorden(self, nodo):
        if nodo:
            yield from self._inorden(nodo.izquierda)
            yield nodo
            yield from self._inorden(nodo.derecha)

    def preorden(self):
        yield from self._preorden(self.raiz)

    def _preorden(self, nodo):
        if nodo:
            yield nodo
            yield from self._preorden(nodo.izquierda)
            yield from self._preorden(nodo.derecha)

    def buscar(self, nombre):
        return self._buscar(self.raiz, nombre)

    def _buscar(self, nodo, nombre):
        if nodo is None:
            return None
        if nombre == nodo.nombre:
            return nodo
        if nombre < nodo.nombre:
            return self._buscar(nodo.izquierda, nombre)
        return self._buscar(nodo.derecha, nombre)

    def eliminar(self, nombre):
        self.raiz, eliminado = self._eliminar(self.raiz, nombre)
        return eliminado

    def _eliminar(self, nodo, nombre):
        if nodo is None:
            return nodo, False
        if nombre < nodo.nombre:
            nodo.izquierda, eliminado = self._eliminar(nodo.izquierda, nombre)
        elif nombre > nodo.nombre:
            nodo.derecha, eliminado = self._eliminar(nodo.derecha, nombre)
        else:
            if nodo.izquierda is None:
                return nodo.derecha, True
            elif nodo.derecha is None:
                return nodo.izquierda, True
            sucesor = self._minimo(nodo.derecha)
            nodo.nombre, nodo.autor, nodo.rol = sucesor.nombre, sucesor.autor, sucesor.rol
            nodo.derecha, _ = self._eliminar(nodo.derecha, sucesor.nombre)
            return nodo, True
        return nodo, eliminado

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

# ============================
# COMANDOS PARA COLABORADORES
# ============================

    def git_add_contributor(self):
        nombre = input("Nombre del colaborador: ")
        autor = input("Email: ")
        rol = input("Rol: ")
        if not self.repositorio_actual.colaboradores:
            self.repositorio_actual.colaboradores = ABBColaboradores()
        self.repositorio_actual.colaboradores.insertar(nombre, autor, rol)
        print(f"[git add-contributor {nombre}] Colaborador agregado.")

    def git_remove_contributor(self):
        nombre = input("Nombre del colaborador a eliminar: ")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        eliminado = self.repositorio_actual.colaboradores.eliminar(nombre)
        if eliminado:
            print(f"[git remove-contributor {nombre}] Eliminado.")
        else:
            print("Colaborador no encontrado.")

    def git_find_contributor(self):
        nombre = input("Nombre a buscar: ")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        nodo = self.repositorio_actual.colaboradores.buscar(nombre)
        if nodo:
            print(f"[git find-contributor {nombre}] Encontrado: {nodo.autor}, rol: {nodo.rol}")
        else:
            print("No encontrado.")

    def git_contributors(self):
        print("[git contributors] Lista de colaboradores:")
        if not self.repositorio_actual.colaboradores:
            print("No hay colaboradores.")
            return
        for nodo in self.repositorio_actual.colaboradores.preorden():
            print(f"- {nodo.nombre} ({nodo.rol}) <{nodo.autor}>")

# ============================
# ESTRUCTURA DE B-TREE (SIMPLIFICADO PARA SHA-1)
# ============================

class NodoBTree:
    def __init__(self, sha, archivo):
        self.sha = sha
        self.archivo = archivo
        self.hijos = ListaEnlazada()  # Punteros a hijos (máx 2 en esta versión simple)

class BTreeArchivos:
    def __init__(self):
        self.raiz = None

    def insertar(self, sha, archivo):
        self.raiz = self._insertar(self.raiz, sha, archivo)

    def _insertar(self, nodo, sha, archivo):
        if nodo is None:
            return NodoBTree(sha, archivo)
        if sha < nodo.sha:
            if nodo.hijos.primero:
                nodo.hijos.primero.dato = self._insertar(nodo.hijos.primero.dato, sha, archivo)
            else:
                nodo.hijos.agregar(self._insertar(None, sha, archivo))
        elif sha > nodo.sha:
            if nodo.hijos.primero and nodo.hijos.primero.siguiente:
                nodo.hijos.primero.siguiente.dato = self._insertar(nodo.hijos.primero.siguiente.dato, sha, archivo)
            else:
                nodo.hijos.agregar(self._insertar(None, sha, archivo))
        return nodo

    def buscar(self, sha):
        return self._buscar(self.raiz, sha)

    def _buscar(self, nodo, sha):
        if nodo is None:
            return None
        if nodo.sha == sha:
            return nodo.archivo
        elif sha < nodo.sha:
            if nodo.hijos.primero:
                return self._buscar(nodo.hijos.primero.dato, sha)
        else:
            if nodo.hijos.primero and nodo.hijos.primero.siguiente:
                return self._buscar(nodo.hijos.primero.siguiente.dato, sha)
        return None

    def preorden(self):
        self._preorden(self.raiz)

    def _preorden(self, nodo):
        if nodo:
            print(f"{nodo.archivo.nombre} (SHA: {nodo.sha})")
            for hijo in nodo.hijos.recorrer():
                self._preorden(hijo)

# ============================
# COMANDOS PARA ARCHIVOS GIT (B-TREE)
# ============================

    def git_file_add(self):
        nombre = input("Nombre del archivo: ")
        contenido = input("Contenido: ")
        archivo = Archivo(nombre, contenido)
        sha = archivo.checksum
        if not self.repositorio_actual.archivos_btree:
            self.repositorio_actual.archivos_btree = BTreeArchivos()
        self.repositorio_actual.archivos_btree.insertar(sha, archivo)
        print(f"[git file-add] Archivo '{nombre}' agregado con SHA {sha}.")

    def git_file_find(self):
        sha = input("SHA-1 del archivo a buscar: ")
        if not self.repositorio_actual.archivos_btree:
            print("No hay archivos.")
            return
        archivo = self.repositorio_actual.archivos_btree.buscar(sha)
        if archivo:
            print(f"Archivo encontrado: {archivo.nombre} | Contenido: {archivo.contenido}")
        else:
            print("Archivo no encontrado.")

    def git_file_list(self):
        print("[git file-list] Archivos almacenados (preorden):")
        if not self.repositorio_actual.archivos_btree:
            print("No hay archivos.")
            return
        self.repositorio_actual.archivos_btree.preorden()

# ============================
# LISTA DE ROLES + AVL DE PERMISOS POR ROL
# ============================

class NodoAVL:
    def __init__(self, email, permisos):
        self.email = email
        self.permisos = permisos  # ListaEnlazada de permisos
        self.altura = 1
        self.izq = None
        self.der = None

class AVLPermisos:
    def __init__(self):
        self.raiz = None

    def insertar(self, email, permisos):
        self.raiz = self._insertar(self.raiz, email, permisos)

    def _insertar(self, nodo, email, permisos):
        if not nodo:
            return NodoAVL(email, permisos)
        if email < nodo.email:
            nodo.izq = self._insertar(nodo.izq, email, permisos)
        else:
            nodo.der = self._insertar(nodo.der, email, permisos)
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))
        return self._balancear(nodo)

    def _altura(self, nodo):
        return nodo.altura if nodo else 0

    def _balancear(self, nodo):
        balance = self._altura(nodo.izq) - self._altura(nodo.der)
        if balance > 1:
            if self._altura(nodo.izq.izq) >= self._altura(nodo.izq.der):
                return self._rotar_derecha(nodo)
            else:
                nodo.izq = self._rotar_izquierda(nodo.izq)
                return self._rotar_derecha(nodo)
        if balance < -1:
            if self._altura(nodo.der.der) >= self._altura(nodo.der.izq):
                return self._rotar_izquierda(nodo)
            else:
                nodo.der = self._rotar_derecha(nodo.der)
                return self._rotar_izquierda(nodo)
        return nodo

    def _rotar_izquierda(self, z):
        y = z.der
        T2 = y.izq
        y.izq = z
        z.der = T2
        z.altura = 1 + max(self._altura(z.izq), self._altura(z.der))
        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        return y

    def _rotar_derecha(self, z):
        y = z.izq
        T3 = y.der
        y.der = z
        z.izq = T3
        z.altura = 1 + max(self._altura(z.izq), self._altura(z.der))
        y.altura = 1 + max(self._altura(y.izq), self._altura(y.der))
        return y

    def buscar(self, email):
        return self._buscar(self.raiz, email)

    def _buscar(self, nodo, email):
        if nodo is None or nodo.email == email:
            return nodo
        if email < nodo.email:
            return self._buscar(nodo.izq, email)
        return self._buscar(nodo.der, email)

    def postorden(self):
        self._postorden(self.raiz)

    def _postorden(self, nodo):
        if nodo is None:
            return
        self._postorden(nodo.izq)
        self._postorden(nodo.der)
        print(f"{nodo.email}: {[p for p in nodo.permisos.recorrer()]}")

class Rol:
    def __init__(self, nombre):
        self.nombre = nombre
        self.permisos_tree = AVLPermisos()

class ListaRoles:
    def __init__(self):
        self.lista = ListaEnlazada()

    def agregar_rol(self, nombre):
        if self.get_rol(nombre) is None:
            self.lista.agregar(Rol(nombre))

    def get_rol(self, nombre):
        return self.lista.buscar(lambda r: r.nombre == nombre)

# ============================
# COMANDOS PARA ROLES Y PERMISOS
# ============================

    def git_role_add(self):
        email = input("Email: ")
        rol_nombre = input("Rol: ")
        permisos = input("Permisos (separados por coma): ").split(",")

        if not self.repositorio_actual.roles_avl:
            self.repositorio_actual.roles_avl = ListaRoles()

        self.repositorio_actual.roles_avl.agregar_rol(rol_nombre)
        rol = self.repositorio_actual.roles_avl.get_rol(rol_nombre)

        permisos_lista = ListaEnlazada()
        for p in permisos:
            permisos_lista.agregar(p.strip())

        rol.permisos_tree.insertar(email, permisos_lista)
        print(f"[git role add {email} {rol_nombre} ...] Permisos asignados.")

    def git_role_update(self):
        email = input("Email: ")
        nuevo_rol = input("Nuevo rol: ")
        nuevos_permisos = input("Nuevos permisos (coma): ").split(",")

        self.git_role_remove(email)
        permisos_lista = ListaEnlazada()
        for p in nuevos_permisos:
            permisos_lista.agregar(p.strip())
        self.repositorio_actual.roles_avl.agregar_rol(nuevo_rol)
        rol = self.repositorio_actual.roles_avl.get_rol(nuevo_rol)
        rol.permisos_tree.insertar(email, permisos_lista)
        print(f"[git role update {email} {nuevo_rol} ...] Rol actualizado.")

    def git_role_remove(self, email=None):
        if email is None:
            email = input("Email: ")

        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            if rol.permisos_tree.buscar(email):
                rol.permisos_tree.raiz = self._eliminar_de_avl(rol.permisos_tree.raiz, email)
                print(f"[git role remove {email}] Eliminado.")
                return
        print("Email no encontrado.")

    def _eliminar_de_avl(self, nodo, email):
        if not nodo:
            return nodo
        if email < nodo.email:
            nodo.izq = self._eliminar_de_avl(nodo.izq, email)
        elif email > nodo.email:
            nodo.der = self._eliminar_de_avl(nodo.der, email)
        else:
            if nodo.izq is None:
                return nodo.der
            elif nodo.der is None:
                return nodo.izq
            temp = nodo.der
            while temp.izq:
                temp = temp.izq
            nodo.email, nodo.permisos = temp.email, temp.permisos
            nodo.der = self._eliminar_de_avl(nodo.der, temp.email)
        return nodo

    def git_role_show(self):
        email = input("Email: ")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            nodo = rol.permisos_tree.buscar(email)
            if nodo:
                print(f"Rol: {rol.nombre}")
                print("Permisos:", ", ".join(p for p in nodo.permisos.recorrer()))
                return
        print("Usuario no encontrado.")

    def git_role_check(self):
        email = input("Email: ")
        accion = input("Acción: ")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            nodo = rol.permisos_tree.buscar(email)
            if nodo:
                if any(p == accion for p in nodo.permisos.recorrer()):
                    print(f"[git role check {email} {accion}] ✅ Permitido")
                    return
        print(f"[git role check {email} {accion}] ❌ Denegado")

    def git_role_list(self):
        print("[git role list] Colaboradores con sus permisos (postorden):")
        for rol in self.repositorio_actual.roles_avl.lista.recorrer():
            print(f"Rol: {rol.nombre}")
            rol.permisos_tree.postorden()

git=GitSystem()
git.ejecutar()
    