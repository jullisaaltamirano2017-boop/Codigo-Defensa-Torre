classDiagram
    direction LR

    class Torre {
        -int id
        -String nombre
        -String tipo
        -int posicion
        -int danio
        -int rango
        -int costo
        +Torre(int, String, String, int, int, int, int)
        +getId() int
        +getNombre() String
        +getTipo() String
        +getPosicion() int
        +getDanio() int
        +getRango() int
        +getCosto() int
        +toString() String
    }

    class Enemigo {
        -int id
        -String tipo
        -int vida
        -int velocidad
        -int posicion
        -int recompensa
        +Enemigo(int, String, int, int, int, int)
        +getId() int
        +getTipo() String
        +getVida() int
        +setVida(int) void
        +getVelocidad() int
        +getPosicion() int
        +setPosicion(int) void
        +getRecompensa() int
        +toString() String
    }

    class Oleada {
        -int idOleada
        -int cantidadEnemigos
        -String tipoEnemigo
        -int vidaBase
        -int velocidadBase
        +Oleada(int, int, String, int, int)
        +getIdOleada() int
        +getCantidadEnemigos() int
        +getTipoEnemigo() String
        +getVidaBase() int
        +getVelocidadBase() int
        +toString() String
    }

    class ListaSecuencialTorres {
        -Torre[] arreglo
        -int tamanio
        -int CAPACIDAD_MAXIMA
        +ListaSecuencialTorres()
        +insertar(Torre) boolean
        +eliminarPorId(int) boolean
        +buscarPorId(int) Torre
        +mostrar() void
        +contarActivas() int
        +getTorre(int) Torre
    }

    class NodoEnemigo {
        -Enemigo enemigo
        -NodoEnemigo anterior
        -NodoEnemigo siguiente
        +NodoEnemigo(Enemigo)
        +getEnemigo() Enemigo
        +setEnemigo(Enemigo) void
        +getAnterior() NodoEnemigo
        +setAnterior(NodoEnemigo) void
        +getSiguiente() NodoEnemigo
        +setSiguiente(NodoEnemigo) void
    }

    class ListaDobleEnemigos {
        -NodoEnemigo primero
        -NodoEnemigo ultimo
        -int tamanio
        +ListaDobleEnemigos()
        +insertarAlFinal(Enemigo) void
        +eliminarPorId(int) boolean
        +buscarPorId(int) Enemigo
        +recorrerAdelante() void
        +recorrerAtras() void
        +getPrimero() NodoEnemigo
        +getTamanio() int
    }

    class NodoOleada {
        -Oleada oleada
        -NodoOleada siguiente
        +NodoOleada(Oleada)
        +getOleada() Oleada
        +setOleada(Oleada) void
        +getSiguiente() NodoOleada
        +setSiguiente(NodoOleada) void
    }

    class ListaCircularOleadas {
        -NodoOleada ultimo
        -NodoOleada oleadaActual
        -int tamanio
        +ListaCircularOleadas()
        +registrar(Oleada) void
        +mostrar() void
        +avanzarSiguienteOleada() Oleada
        +reiniciarCiclo() void
        +getTamanio() int
    }

    class TowerDefenseApp {
        -ListaSecuencialTorres listaTorres
        -ListaDobleEnemigos listaEnemigos
        -ListaCircularOleadas listaOleadas
        -int vidasJugador
        -int FIN_CAMINO
        -int contadorIdEnemigos
        +main(String[] args) void
        -inicializarCasoPrueba() void
        -registrarTorreInteractivo(Scanner) void
        -registrarOleadaInteractivo(Scanner) void
        -iniciarSiguienteOleadaAccion() void
        -avanzarTurno() void
        -mostrarEstadoGeneral() void
    }

    ListaSecuencialTorres "1" o-- "0..50" Torre : "almacena en arreglo"
    NodoEnemigo "1" --> "1" Enemigo : "contiene"
    ListaDobleEnemigos "1" o-- "0..*" NodoEnemigo : "enlaza primero y último"
    NodoOleada "1" --> "1" Oleada : "contiene"
    ListaCircularOleadas "1" o-- "0..*" NodoOleada : "enlaza en bucle circular"
    TowerDefenseApp "1" --> "1" ListaSecuencialTorres : "utiliza"
    TowerDefenseApp "1" --> "1" ListaDobleEnemigos : "utiliza"
    TowerDefenseApp "1" --> "1" ListaCircularOleadas : "utiliza"
