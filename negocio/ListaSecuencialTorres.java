package negocio;

import modelo.Torre;

public class ListaSecuencialTorres {
    private Torre[] arreglo;
    private int tamanio;
    private static final int CAPACIDAD_MAXIMA = 50;

    public ListaSecuencialTorres() {
        arreglo = new Torre[CAPACIDAD_MAXIMA];
        tamanio = 0;
    }

    public boolean insertar(Torre torre) {
        if (tamanio >= CAPACIDAD_MAXIMA) {
            return false;
        }
        arreglo[tamanio++] = torre;
        return true;
    }

    // FIX: antes no existía forma de chequear IDs repetidos antes de insertar,
    // lo que permitía dos torres con el mismo ID (buscarPorId/eliminarPorId solo
    // agarraban la primera y la otra quedaba "fantasma").
    public boolean existeId(int id) {
        return buscarPorId(id) != null;
    }

    public boolean eliminarPorId(int id) {
        int index = -1;
        for (int i = 0; i < tamanio; i++) {
            if (arreglo[i].getId() == id) {
                index = i;
                break;
            }
        }
        if (index == -1) return false;

        for (int i = index; i < tamanio - 1; i++) {
            arreglo[i] = arreglo[i + 1];
        }
        arreglo[--tamanio] = null;
        return true;
    }

    public Torre buscarPorId(int id) {
        for (int i = 0; i < tamanio; i++) {
            if (arreglo[i].getId() == id) {
                return arreglo[i];
            }
        }
        return null;
    }

    public void mostrar() {
        if (tamanio == 0) {
            System.out.println("No hay torres registradas.");
            return;
        }
        for (int i = 0; i < tamanio; i++) {
            System.out.println(arreglo[i]);
        }
    }

    public int contarActivas() {
        return tamanio;
    }

    public Torre getTorre(int index) {
        if (index >= 0 && index < tamanio) {
            return arreglo[index];
        }
        return null;
    }
}
