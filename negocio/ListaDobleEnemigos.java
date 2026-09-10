package negocio;

import modelo.Enemigo;

public class ListaDobleEnemigos {
    private NodoEnemigo primero;
    private NodoEnemigo ultimo;
    private int tamanio;

    public ListaDobleEnemigos() {
        this.primero = null;
        this.ultimo = null;
        this.tamanio = 0;
    }

    public void insertarAlFinal(Enemigo enemigo) {
        NodoEnemigo nuevo = new NodoEnemigo(enemigo);
        if (primero == null) {
            primero = nuevo;
            ultimo = nuevo;
        } else {
            ultimo.setSiguiente(nuevo);
            nuevo.setAnterior(ultimo);
            ultimo = nuevo;
        }
        tamanio++;
    }

    public boolean eliminarPorId(int id) {
        NodoEnemigo actual = primero;
        while (actual != null) {
            if (actual.getEnemigo().getId() == id) {
                if (actual == primero && actual == ultimo) {
                    primero = null;
                    ultimo = null;
                } else if (actual == primero) {
                    primero = primero.getSiguiente();
                    primero.setAnterior(null);
                } else if (actual == ultimo) {
                    ultimo = ultimo.getAnterior();
                    ultimo.setSiguiente(null);
                } else {
                    actual.getAnterior().setSiguiente(actual.getSiguiente());
                    actual.getSiguiente().setAnterior(actual.getAnterior());
                }
                tamanio--;
                return true;
            }
            actual = actual.getSiguiente();
        }
        return false;
    }

    public Enemigo buscarPorId(int id) {
        NodoEnemigo actual = primero;
        while (actual != null) {
            if (actual.getEnemigo().getId() == id) {
                return actual.getEnemigo();
            }
            actual = actual.getSiguiente();
        }
        return null;
    }

    public void recorrerAdelante() {
        if (primero == null) {
            System.out.println("No hay enemigos activos.");
            return;
        }
        NodoEnemigo actual = primero;
        while (actual != null) {
            System.out.println(actual.getEnemigo());
            actual = actual.getSiguiente();
        }
    }

    public void recorrerAtras() {
        if (ultimo == null) {
            System.out.println("No hay enemigos activos.");
            return;
        }
        NodoEnemigo actual = ultimo;
        while (actual != null) {
            System.out.println(actual.getEnemigo());
            actual = actual.getAnterior();
        }
    }

    public NodoEnemigo getPrimero() { return primero; }
    public int getTamanio() { return tamanio; }
}