package negocio;
import modelo.Torre;

public class ListaSecuencialTorres {
    private Torre[] arreglo;
    private int tamanio;

    public ListaSecuencialTorres() {
        arreglo = new Torre[10];
        tamanio = 0;
    }
    public boolean insertar(Torre torre) {

        if (tamanio >= arreglo.length) {
            return false;
        }

        arreglo[tamanio] = torre;
        tamanio++;

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

        for (int i = 0; i < tamanio; i++) {
            System.out.println(arreglo[i]);
        }
    }
    public int contarActivas() {
        return tamanio;
    }
}