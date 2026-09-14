class Oleada:
    def __init__(self, id_oleada, cantidad_enemigos, tipo_enemigo, vida_base, velocidad_base):
        self.id_oleada = id_oleada
        self.cantidad_enemigos = cantidad_enemigos
        self.tipo_enemigo = tipo_enemigo
        self.vida_base = vida_base
        self.velocidad_base = velocidad_base

    def __str__(self):
        return (f"Oleada [ID={self.id_oleada}, Cantidad={self.cantidad_enemigos}, "
                f"Tipo={self.tipo_enemigo}, VidaBase={self.vida_base}, "
                f"VelocidadBase={self.velocidad_base}]")