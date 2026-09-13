# Código Defensa Torre (Tower Defense)

Prueba práctica de Estructuras de Datos aplicada a un videojuego bajo el paradigma de Programación Orientada a Objetos (POO).

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#1-descripción-del-proyecto)
2. [Arquitectura y Paquetes](#2-arquitectura-y-paquetes)
3. [Estructuras de Datos Implementadas](#3-estructuras-de-datos-implementadas)
4. [Diagrama del Sistema](#4-diagrama-del-sistema)
5. [Requisitos y Ejecución](#5-requisitos-y-ejecución)

---

## 1. Descripción del Proyecto

**Código Defensa Torre** es una aplicación desarrollada en **Python** que simula la lógica de control de un juego del género **Tower Defense**. El sistema gestiona entidades clave como torres defensivas, unidades enemigas y oleadas tácticas mediante el uso exclusivo de **estructuras de datos hechas desde cero**, evitando depender de librerías o contenedores avanzados predeterminados para la lógica fundamental de negocio.

---

## 2. Arquitectura y Paquetes

El proyecto se encuentra organizado de manera modular dentro del directorio `Python/`, separando claramente la interfaz gráfica o de control, las entidades del modelo de dominio y las estructuras de negocio:

```text
Codigo-Defensa-Torre/
├── Diagrama/
│   └── diagrama.md                # Documentación gráfica de clases (Mermaid)
└── Python/
    ├── app/
    │   └── tower_defense_gui.py       # Controlador principal e interfaz de usuario
    ├── modelo/
    │   ├── torre.py                   # Entidad que define atributos y métodos de las torres
    │   ├── enemigo.py                 # Entidad que define atributos y estados de los enemigos
    │   └── oleada.py                  # Entidad que agrupa los parámetros de las oleadas
    └── negocio/
        ├── ListaSecuencialTorres.py   # Gestión estática de torres mediante arreglos
        ├── NodoEnemigo.py             # Nodo bidireccional auxiliar para enemigos
        ├── lista_doble_enemigos.py    # Gestión dinámica de enemigos con lista doblemente enlazada
        ├── nodo_oleada.py             # Nodo auxiliar para soporte de estructuras circulares
        └── lista_circular_oleadas.py  # Gestión cíclica y continua de las oleadas de enemigos[cite: 3]
