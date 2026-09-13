```mermaid
classDiagram
    direction LR

    class Torre {
        -int id
        -str nombre
        -str tipo
        -int posicion
        -int danio
        -int rango
        -int costo
        +__init__(id, nombre, tipo, posicion, danio, rango, costo)
        +get_id() int
        +get_nombre() str
        +get_tipo() str
        +get_posicion() int
        +get_danio() int
        +get_rango() int
        +get_costo() int
        +__str__() str
    }

    class Enemigo {
        -int id
        -str tipo
        -int vida
        -int velocidad
        -int posicion
        -int recompensa
        +__init__(id, tipo, vida, velocidad, posicion, recompensa)
        +get_id() int
        +get_tipo() str
        +get_vida() int
        +set_vida(vida) void
        +get_velocidad() int
        +get_posicion() int
        +set_posicion(posicion) void
        +get_recompensa() int
        +__str__() str
    }

    class Oleada {
        -int id_oleada
        -int cantidad_enemigos
        -str tipo_enemigo
        -int vida_base
        -int velocidad_base
        +__init__(id_oleada, cantidad_enemigos, tipo_enemigo, vida_base, velocidad_base)
        +get_id_oleada() int
        +get_cantidad_enemigos() int
        +get_tipo_enemigo() str
        +get_vida_base() int
        +get_velocidad_base() int
        +__str__() str
    }

    class ListaSecuencialTorres {
        -list arreglo
        -int tamanio
        -int capacidad_maxima
        +__init__(capacidad_maxima)
        +insertar(torre) bool
        +eliminar_por_id(id) bool
        +buscar_por_id(id) Torre
        +mostrar() void
        +contar_activas() int
        +get_torre(indice) Torre
    }

    class NodoEnemigo {
        -Enemigo enemigo
        -NodoEnemigo anterior
        -NodoEnemigo siguiente
        +__init__(enemigo)
        +get_enemigo() Enemigo
        +set_enemigo(enemigo) void
        +get_anterior() NodoEnemigo
        +set_anterior(nodo) void
        +get_siguiente() NodoEnemigo
        +set_siguiente(nodo) void
    }

    class ListaDobleEnemigos {
        -NodoEnemigo primero
        -NodoEnemigo ultimo
        -int tamanio
        +__init__()
        +insertar_al_final(enemigo) void
        +eliminar_por_id(id) bool
        +buscar_por_id(id) Enemigo
        +recorrer_adelante() void
        +recorrer_atras() void
        +get_primero() NodoEnemigo
        +get_tamanio() int
    }

    class NodoOleada {
        -Oleada oleada
        -NodoOleada siguiente
        +__init__(oleada)
        +get_oleada() Oleada
        +set_oleada(oleada) void
        +get_siguiente() NodoOleada
        +set_siguiente(nodo) void
    }

    class ListaCircularOleadas {
        -NodoOleada ultimo
        -NodoOleada oleada_actual
        -int tamanio
        +__init__()
        +registrar(oleada) void
        +mostrar() void
        +avanzar_siguiente_oleada() Oleada
        +reiniciar_ciclo() void
        +get_tamanio() int
    }

    class TowerDefenseGUI {
        -ListaSecuencialTorres lista_torres
        -ListaDobleEnemigos lista_enemigos
        -ListaCircularOleadas lista_oleadas
        -int vidas_jugador
        -int fin_camino
        +__init__(root)
        +inicializar_caso_prueba() void
        +ejecutar() void
    }

    ListaSecuencialTorres "1" o-- "0..50" Torre : "almacena en arreglo"
    NodoEnemigo "1" --> "1" Enemigo : "contiene"
    ListaDobleEnemigos "1" o-- "0..*" NodoEnemigo : "enlaza primero y último"
    NodoOleada "1" --> "1" Oleada : "contiene"
    ListaCircularOleadas "1" o-- "0..*" NodoOleada : "enlaza en bucle circular"
    TowerDefenseGUI "1" --> "1" ListaSecuencialTorres : "utiliza"
    TowerDefenseGUI "1" --> "1" ListaDobleEnemigos : "utiliza"
    TowerDefenseGUI "1" --> "1" ListaCircularOleadas : "utiliza"
