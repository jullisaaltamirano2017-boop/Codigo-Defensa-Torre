package negocio;

import modelo.Oleada;

public class ListaCircularOleadas {
    private NodoOleada ultimo;
    private NodoOleada oleadaActual;
    private int tamanio;

    public ListaCircularOleadas() {
        this.ultimo = null;
        this.oleadaActual = null;
        this.tamanio = 0;
    }

    public void registrar(Oleada oleada) {
        NodoOleada nuevo = new NodoOleada(oleada);
        if (ultimo == null) {
            ultimo = nuevo;
            ultimo.setSiguiente(ultimo);
            oleadaActual = ultimo;
        } else {
            nuevo.setSiguiente(ultimo.getSiguiente());
            ultimo.setSiguiente(nuevo);
            ultimo = nuevo;
        }
        tamanio++;
    }

    // FIX: no había forma de saber si un ID de oleada ya existía antes de
    // registrar otra igual (mismo problema que en ListaSecuencialTorres).
    public boolean existeId(int idOleada) {
        if (ultimo == null) return false;
        NodoOleada actual = ultimo.getSiguiente();
        do {
            if (actual.getOleada().getIdOleada() == idOleada) {
                return true;
            }
            actual = actual.getSiguiente();
        } while (actual != ultimo.getSiguiente());
        return false;
    }

    public void mostrar() {
        if (ultimo == null) {
            System.out.println("No hay oleadas registradas.");
            return;
        }
        NodoOleada actual = ultimo.getSiguiente();
        do {
            System.out.println(actual.getOleada());
            actual = actual.getSiguiente();
        } while (actual != ultimo.getSiguiente());
    }

    public Oleada avanzarSiguienteOleada() {
        if (ultimo == null) return null;
        Oleada actual = oleadaActual.getOleada();
        oleadaActual = oleadaActual.getSiguiente();
        return actual;
    }

    public void reiniciarCiclo() {
        if (ultimo != null) {
            oleadaActual = ultimo.getSiguiente();
        }
    }

    public int getTamanio() { return tamanio; }
}
