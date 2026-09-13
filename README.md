# Código Defensa Torre (Tower Defense)

Prueba práctica de Estructuras de datos para un videojuego.

---

## Tabla de Contenidos

1. [Descripción del Proyecto](#1-descripción-del-proyecto)
2. [Arquitectura y Paquetes](#2-arquitectura-y-paquetes)
3. [Estructuras de Datos Implementadas](#3-estructuras-de-datos-implementadas)
4. [Diagrama del Sistema](#4-diagrama-del-sistema)
5. [Requisitos y Ejecución](#5-requisitos-y-ejecución)

---

## 1. Descripción del Proyecto

**Código Defensa Torre** es una aplicación desarrollada en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)**. El sistema simula la lógica de control de un juego de defensa de torres, gestionando entidades clave como torres de defensa, enemigos y oleadas mediante el uso exclusivo de **estructuras de datos hechas desde cero** sin depender de colecciones predeterminadas avanzadas para la lógica principal de negocio.

---

## 2. Arquitectura y Paquetes

El proyecto se encuentra estructurado de manera modular dentro del directorio de Python para separar la interfaz, las entidades del modelo y la lógica de negocio:

```text
Codigo-Defensa-Torre/
└── Python/
    ├── app/
    │   ├── tower_defense_gui.py       # Interfaz principal de la aplicación
    │   └── lista_circular_oleadas.py  # Funcionalidad auxiliar de control de oleadas
    ├── modelo/
    │   ├── enemigo.py                 # Entidad que define atributos y estados de los enemigos
    │   └── oleada.py                  # Entidad que agrupa y administra las oleadas
    └── negocio/
        ├── ListaSecuencialTorres.py   # Gestión de torres mediante arreglos o listas secuenciales
        ├── NodoEnemigo.py             # Nodo auxiliar bidireccional para enemigos
        ├── lista_doble_enemigos.py    # Gestión dinámica de enemigos con lista doblemente enlazada
        └── nodo_oleada.py             # Nodo auxiliar para soportar operaciones circulares[cite: 2]
