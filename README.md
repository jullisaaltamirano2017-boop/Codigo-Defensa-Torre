# Código Defensa Torre (Tower Defense)

<p align="center">
  <b>Prueba práctica de Estructuras de datos para un videojuego</b>
</p>

---

## Tabla de Contenidos
1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Arquitectura y Paquetes](#-arquitectura-y-paquetes)
3. [Estructuras de Datos Implementadas](#-estructuras-de-datos-implementadas)
4. [Diagrama del Sistema](#-diagrama-del-sistema)
5. [Requisitos y Ejecución](#-requisitos-y-ejecución)

---

## Descripción del Proyecto

**Código Defensa Torre** es una aplicación desarrollada en **Java** bajo el paradigma de **Programación Orientada a Objetos (POO)**. El sistema simula la lógica de control de un juego de defensa de torres, gestionando entidades clave como torres de defensa, enemigos y oleadas mediante el uso exclusivo de **estructuras de datos hechas desde cero** sin depender de las colecciones predeterminadas de Java como `ArrayList` o `LinkedList` para la lógica principal de negocio.

---

## Arquitectura y Paquetes

El proyecto se encuentra estructurado de manera modular para separar la interfaz de usuario, las entidades del modelo y la lógica de negocio:

```text
Codigo-Defensa-Torre/
│
├── app/
│   └── TowerDefenseApp.java          # Clase principal con la interfaz de consola e interacción (Scanner)
│
├── modelo/
│   ├── Torre.java                    # Entidad que define atributos y métodos de las torres
│   ├── Enemigo.java                  # Entidad que define atributos y estados de los enemigos
│   └── Oleada.java                   # Entidad que agrupa y administra las oleadas
│
├── negocio/
│   ├── ListaSecuencialTorres.java    # Gestión de torres mediante arreglos/listas secuenciales
│   ├── ListaDobleEnemigos.java       # Gestión dinámica de enemigos con lista doblemente enlazada
│   ├── ListaCircularOleadas.java     # Gestión cíclica de las oleadas del juego
│   ├── NodoEnemigo.java              # Nodo para la lista doble de enemigos
│   └── NodoOleada.java               # Nodo para la lista circular de oleadas
│
└── Diagrama/
    └── Diagrama.md                   # Documentación gráfica y esquemas UML del sistema
