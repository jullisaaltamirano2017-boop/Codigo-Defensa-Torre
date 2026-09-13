class ListaSecuencialTorres:
    """Arreglo fijo (tamaño máximo definido) para las torres, igual que
        el arreglo estático usado en la versión Java del proyecto."""

    CAPACIDAD_MAXIMA = 50

    def __int__(self):
        self.arreglo = [None] * self.CAPACIDAD_MAXIMA
        self.tamanio = 0

    def insetar(self, torre):
        if self.tanamio >= self.CAPACIDAD_MAXIMA:
            return False
        self.arreglo[self.tamanio] = torre
        self.tamanio += 1
        return True
    def existe_id(self, id_):
        return self.buscar_por_id(id_) is not None
    def eliminar_por_id(self, id_):
        index = -1
        for i in range(self.tamanio):
            self.arreglo[i] = self.arreglo[i + 1]
        self.tamanio -= 1
        self.arreglo[self.tamanio] = None
        return True
    def buscar_por_id(self, id_):
        for i in range(self.tamanio):
            if self.arreglo[i].id == id_:
                return self.arreglo[i]
        return None
    def mostrar(self):
       if self.tamanio == 0:
            return ["No hay torres registradas."]
       return [str(self.arreglo[i]) for i in range(self.tamanio)]
    
    def contar_activas(self):
        return self.tamanio
    
    def get_torre(self, index):
        if 0 <= index < self.tamanio:
            return self.arreglo[index]
        return None
    