from negocio.nodo_oleada import NodoOleada


class ListaCircularOleadas:
    """Lista simplemente enlazada circular para las oleadas, igual que
    en la versión Java: al llegar a la última oleada registrada, el
    ciclo vuelve a la primera automáticamente."""

    def __init__(self):
        self.ultimo = None
        self.oleada_actual = None
        self.tamanio = 0

    def registrar(self, oleada):
        nuevo = NodoOleada(oleada)
        if self.ultimo is None:
            self.ultimo = nuevo
            self.ultimo.siguiente = self.ultimo
            self.oleada_actual = self.ultimo
        else:
            nuevo.siguiente = self.ultimo.siguiente
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo
        self.tamanio += 1

    def existe_id(self, id_oleada):
        if self.ultimo is None:
            return False
        actual = self.ultimo.siguiente
        while True:
            if actual.oleada.id_oleada == id_oleada:
                return True
            actual = actual.siguiente
            if actual is self.ultimo.siguiente:
                break
        return False

    def mostrar(self):
        if self.ultimo is None:
            return ["No hay oleadas registradas."]
        lineas = []
        actual = self.ultimo.siguiente
        while True:
            lineas.append(str(actual.oleada))
            actual = actual.siguiente
            if actual is self.ultimo.siguiente:
                break
        return lineas

    def avanzar_siguiente_oleada(self):
        if self.ultimo is None:
            return None
        actual = self.oleada_actual.oleada
        self.oleada_actual = self.oleada_actual.siguiente
        return actual

    def reiniciar_ciclo(self):
        if self.ultimo is not None:
            self.oleada_actual = self.ultimo.siguiente

    def get_tamanio(self):
        return self.tamanio
