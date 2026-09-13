from negocio.nodo_enemigo import NodoEnemigo

class ListaDobleEnemigos:
    """Lista doblemente enlazada manual para los enemigos activos en
    el campo, igual que en la versión Java."""

    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.tamanio = 0

    def insertar_al_final(self, enemigo):
        nuevo = NodoEnemigo(enemigo)
        if self.primero is None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.tamanio += 1

    def eliminar_por_id(self, id_):
        actual = self.primero
        while actual is not None:
            if actual.enemigo.id == id_:
                if actual is self.primero and actual is self.ultimo:
                    self.primero = None
                    self.ultimo = None
                elif actual is self.primero:
                    self.primero = self.primero.siguiente
                    self.primero.anterior = None
                elif actual is self.ultimo:
                    self.ultimo = self.ultimo.anterior
                    self.ultimo.siguiente = None
                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior
                self.tamanio -= 1
                return True
            actual = actual.siguiente
        return False

    def buscar_por_id(self, id_):
        actual = self.primero
        while actual is not None:
            if actual.enemigo.id == id_:
                return actual.enemigo
            actual = actual.siguiente
        return None

    def recorrer_adelante(self):
        if self.primero is None:
            return ["No hay enemigos activos."]
        lineas = []
        actual = self.primero
        while actual is not None:
            lineas.append(str(actual.enemigo))
            actual = actual.siguiente
        return lineas

    def recorrer_atras(self):
        if self.ultimo is None:
            return ["No hay enemigos activos."]
        lineas = []
        actual = self.ultimo
        while actual is not None:
            lineas.append(str(actual.enemigo))
            actual = actual.anterior
        return lineas

    def get_primero(self):
        return self.primero

    def get_tamanio(self):
        return self.tamanio
