class Enemigo:
    def __init__(self, id_, tipo, vida, velocidad, posicion, recompensa):
        self.id = id_
        self.tipo = tipo
        self.vida = vida
        self.velocidad = velocidad
        self.posicion = posicion
        self.recompensa = recompensa

    def __str__(self):
        return (f"Enemigo [ID={self.id}, Tipo={self.tipo}, Vida={self.vida}, "
                f"Velocidad={self.velocidad}, Pos={self.posicion}, "
                f"Recompensa={self.recompensa}]")