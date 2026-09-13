class Torre:
    def __init__(self, id_, nombre, tipo, posicion, danio, rango, costo):
        self.id = id_
        self.nombre = nombre
        self.tipo = tipo
        self.posicion = posicion
        self.danio = danio
        self.rango = rango
        self.costo = costo

    def __str__(self):
        return (f"Torre [ID={self.id}, Nombre={self.nombre}, Tipo={self.tipo}, "
                f"Pos={self.posicion}, Daño={self.danio}, Rango={self.rango}, "
                f"Costo={self.costo}]")
