package main;

import modelo.Torre;
import modelo.Enemigo;
import modelo.Oleada;
import negocio.ListaSecuencialTorres;
import negocio.ListaDobleEnemigos;
import negocio.ListaCircularOleadas;
import negocio.NodoEnemigo;

import java.util.Scanner;

public class TowerDefenseApp {
    private static ListaSecuencialTorres listaTorres = new ListaSecuencialTorres();
    private static ListaDobleEnemigos listaEnemigos = new ListaDobleEnemigos();
    private static ListaCircularOleadas listaOleadas = new ListaCircularOleadas();
    private static int vidasJugador = 3;
    private static final int FIN_CAMINO = 20;
    private static int contadorIdEnemigos = 1;

    public static void main(String[] args) {
        inicializarCasoPrueba();
        Scanner scanner = new Scanner(System.in);
        int opcion = 0;

        do {
            System.out.println("\n--- TOWER DEFENSE - MENÚ PRINCIPAL ---");
            System.out.println("1. Registrar torre defensiva");
            System.out.println("2. Mostrar torres registradas");
            System.out.println("3. Eliminar torre");
            System.out.println("4. Registrar oleada");
            System.out.println("5. Mostrar oleadas");
            System.out.println("6. Iniciar siguiente oleada");
            System.out.println("7. Avanzar turno");
            System.out.println("8. Mostrar enemigos activos");
            System.out.println("9. Mostrar estado general del juego");
            System.out.println("10. Salir");
            System.out.print("Seleccione una opción: ");

            if (scanner.hasNextInt()) {
                opcion = scanner.nextInt();
                scanner.nextLine(); // limpiar buffer
            } else {
                System.out.println("Por favor, ingrese un número válido.");
                scanner.nextLine();
                continue;
            }

            switch (opcion) {
                case 1:
                    registrarTorreInteractivo(scanner);
                    break;
                case 2:
                    System.out.println("\n--- TORRES REGISTRADAS ---");
                    listaTorres.mostrar();
                    break;
                case 3:
                    // FIX: antes usaba scanner.nextInt() sin validar -> si el usuario
                    // metía texto en vez de un número, reventaba con InputMismatchException.
                    int idTorre = leerEntero(scanner, "Ingrese ID de la torre a eliminar: ");
                    if (listaTorres.eliminarPorId(idTorre)) {
                        System.out.println("Torre eliminada con éxito.");
                    } else {
                        System.out.println("No se encontró la torre con ID especificado.");
                    }
                    break;
                case 4:
                    registrarOleadaInteractivo(scanner);
                    break;
                case 5:
                    System.out.println("\n--- OLEADAS REGISTRADAS ---");
                    listaOleadas.mostrar();
                    break;
                case 6:
                    iniciarSiguienteOleadaAccion();
                    break;
                case 7:
                    avanzarTurno();
                    break;
                case 8:
                    System.out.println("\n--- ENEMIGOS ACTIVOS ---");
                    listaEnemigos.recorrerAdelante();
                    break;
                case 9:
                    mostrarEstadoGeneral();
                    break;
                case 10:
                    System.out.println("¡Gracias por jugar!");
                    break;
                default:
                    System.out.println("Opción inválida.");
            }

            if (vidasJugador <= 0) {
                System.out.println("\n[!] ¡HAS PERDIDO TODAS TUS VIDAS! Game Over.");
                break;
            }

        } while (opcion != 10);
        scanner.close();
    }

    // FIX: helper nuevo. Reemplaza los scanner.nextInt() sueltos que no
    // validaban nada. Se queda pidiendo el dato hasta que sea un número real,
    // y siempre limpia el buffer (evita el problema clásico de nextInt()
    // dejando el '\n' pendiente antes de un nextLine()).
    private static int leerEntero(Scanner scanner, String mensaje) {
        while (true) {
            System.out.print(mensaje);
            if (scanner.hasNextInt()) {
                int valor = scanner.nextInt();
                scanner.nextLine();
                return valor;
            } else {
                System.out.println("Eso no es un número válido, intenta de nuevo.");
                scanner.nextLine();
            }
        }
    }

    private static void inicializarCasoPrueba() {
        // Torres iniciales
        listaTorres.insertar(new Torre(1, "Arquero", "Fisico", 3, 20, 2, 50));
        listaTorres.insertar(new Torre(2, "Cañón", "Explosivo", 8, 35, 3, 100));

        // Oleadas iniciales
        listaOleadas.registrar(new Oleada(1, 3, "Básico", 50, 1));
        listaOleadas.registrar(new Oleada(2, 2, "Rápido", 40, 2));

        System.out.println("[i] Caso de prueba inicial cargado correctamente.");
    }

    private static void registrarTorreInteractivo(Scanner scanner) {
        int id = leerEntero(scanner, "ID de torre: ");

        // FIX: antes no se validaba si el ID ya existía. Dos torres con el
        // mismo ID rompían buscarPorId/eliminarPorId (solo agarraban la primera).
        if (listaTorres.existeId(id)) {
            System.out.println("Ya existe una torre con ese ID. Operación cancelada.");
            return;
        }

        System.out.print("Nombre de la torre: ");
        String nombre = scanner.nextLine();
        System.out.print("Tipo: ");
        String tipo = scanner.nextLine();
        int posicion = leerEntero(scanner, "Posición en la ruta (0 - 20): ");
        int danio = leerEntero(scanner, "Daño: ");
        int rango = leerEntero(scanner, "Rango de alcance: ");
        int costo = leerEntero(scanner, "Costo: ");

        Torre nueva = new Torre(id, nombre, tipo, posicion, danio, rango, costo);
        if (listaTorres.insertar(nueva)) {
            System.out.println("¡Torre registrada con éxito!");
        } else {
            System.out.println("Capacidad máxima de torres alcanzada.");
        }
    }

    private static void registrarOleadaInteractivo(Scanner scanner) {
        int id = leerEntero(scanner, "ID de oleada: ");

        // FIX: mismo chequeo de ID duplicado, ahora para oleadas.
        if (listaOleadas.existeId(id)) {
            System.out.println("Ya existe una oleada con ese ID. Operación cancelada.");
            return;
        }

        int cant = leerEntero(scanner, "Cantidad de enemigos: ");
        System.out.print("Tipo de enemigo: ");
        String tipo = scanner.nextLine();
        int vida = leerEntero(scanner, "Vida base: ");
        int vel = leerEntero(scanner, "Velocidad base: ");

        Oleada oleada = new Oleada(id, cant, tipo, vida, vel);
        listaOleadas.registrar(oleada);
        System.out.println("¡Oleada registrada con éxito!");
    }

    private static void iniciarSiguienteOleadaAccion() {
        Oleada oleada = listaOleadas.avanzarSiguienteOleada();
        if (oleada == null) {
            System.out.println("No hay oleadas disponibles.");
            return;
        }
        System.out.println("\n[!] ¡Iniciando Oleada " + oleada.getIdOleada() + " (" + oleada.getTipoEnemigo() + ")!");
        for (int i = 0; i < oleada.getCantidadEnemigos(); i++) {
            Enemigo e = new Enemigo(contadorIdEnemigos++, oleada.getTipoEnemigo(), oleada.getVidaBase(), oleada.getVelocidadBase(), 0, 10);
            listaEnemigos.insertarAlFinal(e);
        }
        System.out.println("Se han generado " + oleada.getCantidadEnemigos() + " enemigos en la posición 0.");
    }

    private static void avanzarTurno() {
        if (listaEnemigos.getTamanio() == 0) {
            System.out.println("No hay enemigos activos en el campo. Inicie una oleada primero.");
            return;
        }

        System.out.println("\n--- EJECUTANDO TURNO ---");

        // 1. Mover enemigos
        NodoEnemigo actual = listaEnemigos.getPrimero();
        while (actual != null) {
            Enemigo e = actual.getEnemigo();
            e.setPosicion(e.getPosicion() + e.getVelocidad());
            actual = actual.getSiguiente();
        }

        // 2 y 3. Torres atacan enemigos en rango
        for (int i = 0; i < listaTorres.contarActivas(); i++) {
            Torre t = listaTorres.getTorre(i);
            NodoEnemigo nodoE = listaEnemigos.getPrimero();
            while (nodoE != null) {
                Enemigo e = nodoE.getEnemigo();
                int distancia = Math.abs(e.getPosicion() - t.getPosicion());
                if (distancia <= t.getRango() && e.getVida() > 0) {
                    int nuevaVida = e.getVida() - t.getDanio();
                    e.setVida(Math.max(0, nuevaVida));
                    System.out.println("-> Torre " + t.getNombre() + " atacó al Enemigo ID " + e.getId() + " (-" + t.getDanio() + " HP). Vida restante: " + e.getVida());
                }
                nodoE = nodoE.getSiguiente();
            }
        }

        // 4 y 5. Eliminar enemigos muertos o evaluar fin de ruta
        NodoEnemigo actualEval = listaEnemigos.getPrimero();
        while (actualEval != null) {
            NodoEnemigo siguienteEval = actualEval.getSiguiente();
            Enemigo e = actualEval.getEnemigo();

            if (e.getVida() <= 0) {
                System.out.println("[x] ¡Enemigo ID " + e.getId() + " (" + e.getTipo() + ") ha sido destruido!");
                listaEnemigos.eliminarPorId(e.getId());
            } else if (e.getPosicion() >= FIN_CAMINO) {
                System.out.println("[!] ¡Enemigo ID " + e.getId() + " llegó al final del camino! Pierdes 1 vida.");
                vidasJugador--;
                listaEnemigos.eliminarPorId(e.getId());
            }

            actualEval = siguienteEval;
        }

        System.out.println("Turno finalizado. Vidas actuales del jugador: " + vidasJugador);
    }

    private static void mostrarEstadoGeneral() {
        System.out.println("\n====== ESTADO GENERAL DEL JUEGO ======");
        System.out.println("Vidas del Jugador: " + vidasJugador);
        System.out.println("Torres Activas: " + listaTorres.contarActivas());
        System.out.println("Enemigos Activos en Campo: " + listaEnemigos.getTamanio());
        System.out.println("----------------------------------------");
    }
}
