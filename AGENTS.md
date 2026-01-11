# 🤖 Agent Guidelines: Sistema de Gestión de Competencias

Este documento define las directrices, arquitectura y estándares para el desarrollo del backend de la API de Competencias. Estas reglas son de cumplimiento obligatorio para garantizar la calidad y mantenibilidad del software.

---

## 🎯 Objetivo del Sistema
Construir una API REST robusta encargada de gestionar competidores y automatizar la creación de emparejamientos en estructuras de pirámide (brackets), garantizando lógica matemática e integridad de datos.

## 🛠 Stack Tecnológico
- **Lenguaje:** Python 3.13+
- **Gestor de Paquetes:** `uv` (Fastest Python package manager)
- **Framework Web:** FastAPI
- **Validación:** Pydantic V2 (con soporte nativo para CamelCase en la frontera del API)
- **Testing:** Pytest

---

## 🏗 Arquitectura: Domain-Driven Design (DDD)
El proyecto se organiza en capas para proteger la lógica de negocio de los detalles tecnológicos:

### 1. Capa de Dominio (`/domain`)
- **Contenido:** Entidades (Competidor, Partido, Piramide), Objetos de Valor (Email, Ranking), y excepciones de dominio.
- **Regla de Oro:** 0 dependencias externas. No debe importar FastAPI, SQLAlchemy o Pydantic (si se usa para persistencia). Es Python puro.

### 2. Capa de Aplicación (`/application`)
- **Contenido:** Casos de uso (ej. `GenerarCrucesDeTorneo`, `RegistrarResultado`).
- **Función:** Orquestar el flujo de datos entre el dominio y la infraestructura.

### 3. Capa de Infraestructura (`/infrastructure`)
- **Contenido:** Repositorios de base de datos, adaptadores de servicios externos.
- **Función:** Implementar los detalles técnicos que el dominio requiere mediante interfaces.

### 4. Capa de Interfaz / Entrypoints (`/api`)
- **Contenido:** Rutas de FastAPI, Middlewares y Esquemas Pydantic.



---

## 🧪 Metodología: Test-Driven Development (TDD)
No se escribe código de producción sin una prueba que lo justifique. Se seguirá el ciclo **Red-Green-Refactor**:

1.  **Red:** Escribir un test que falle en `backend/tests/`.
2.  **Green:** Implementar el código mínimo para que el test pase.
3.  **Refactor:** Optimizar el código manteniendo los tests en verde.

> **Nota:** Se priorizarán los tests unitarios sobre la lógica de generación de pirámides para asegurar que los algoritmos de cruces sean infalibles.

---

## 📜 Convenciones y Estándares
- **Tipado:** Type Hints obligatorios en firmas de funciones y métodos.
- **Nomenclatura:**
    - Python: `snake_case` (interno).
    - JSON: `camelCase` (externo para compatibilidad con Vue).
- **Inyección de Dependencias:** Se utilizará el sistema de `Depends` de FastAPI para desacoplar controladores de servicios.
- **Modelos:** Todos los esquemas de respuesta deben heredar de un `TunedModel` base que convierta automáticamente a CamelCase.

---

## 🚀 Comandos de Referencia
- **Sincronizar entorno:** `uv sync`
- **Ejecutar Tests:** `uv run pytest`
- **Levantar Servidor:** `uv run uvicorn app.main:app --reload`

## 📊 Modelo de Datos y Entidades (Contexto de Persistencia)

El sistema se basa en un esquema de PostgreSQL (v17) que define la logística de torneos. Las entidades deben ser mapeadas al Dominio respetando las siguientes relaciones y restricciones:

### 1. Núcleo de Identidad y Membresía
* **Person**: Entidad base de identidad con `firstname` y `lastname`.
* **Academy**: Vinculada a un Instructor (tipo `person`). Es la entidad de pertenencia de los competidores.
* **Competitor**: Estudiante vinculado a una `person`, una `academy`, un `rank` (grado) y un `sex`. Incluye métricas físicas: `age`, `weight` y `height`.

### 2. Estructura de Competencia (Categorización)
* **Category**: Define el grupo de competencia mediante rangos de edad (`initial_age` a `final_age`) y peso (`initial_weight` a `final_weight`). Está vinculada a una **Modality** (ej. Combate o Formas).
* **Category_Rank / Category_Sex**: Tablas intermedias que restringen qué grados y sexos pueden participar en una categoría específica.
* **Championship**: El evento macro. Los competidores se inscriben mediante la tabla **Competitor_Category**, que vincula al atleta con una categoría y un campeonato.

### 3. Lógica de Eliminación (Pirámide)
* **Round**: Define las etapas del torneo: *Octavos de Final, Cuartos de Final, Semi Final y Final*.
* **Pyramid**: Representa los enfrentamientos (brackets).
    * Relaciona un `first_competitor` y un `second_competitor` (referenciando a `competitor_category`).
    * Rastrea el progreso mediante la columna `winner`.
    * **Restricción de Integridad**: Un competidor solo puede aparecer una vez por cada ronda (`round`) dentro de su categoría.

### 🧠 Reglas de Negocio para el Dominio (DDD)
1.  **Validación de Categoría**: Antes de inscribir a un competidor, el dominio debe validar que su `age`, `weight`, `sex` y `rank` coincidan con los rangos permitidos por la `Category`.
2.  **Generación de Brackets**: La lógica debe garantizar que el número de competidores sea potencia de 2 ($2^n$), o gestionar adecuadamente los "Byes" (pases directos) cuando el `second_competitor` sea nulo en la primera ronda.
3.  **UUIDs**: Se utiliza `UUID` como estándar para todas las claves primarias, permitiendo la generación de identidades en la capa de aplicación sin depender de la base de datos.
4.  

# Estructura de archivos:

Esta estructura organiza el código por responsabilidades de negocio (Features), permitiendo que la lógica de la pirámide sea independiente de la gestión de academias.

backend/
├── 📁 src/
│   ├── 📁 core/                   <-- LÓGICA TRANSVERSAL (Configuración y Base)
│   │   ├── 📜 config.py           # Configuración con Pydantic Settings (ENVs)
│   │   ├── 📜 database.py         # Conexión a PostgreSQL y sesión de SQLAlchemy
│   │   ├── 📜 security.py         # Gestión de JWT y hashing
│   │   └── 📁 common/             
│   │       ├── 📜 models.py       # TunedModel (Base para CamelCase de Pydantic)
│   │       └── 📜 exceptions.py   # Manejadores de errores globales
│   │
│   ├── 📁 features/               <-- MÓDULOS DE NEGOCIO (Basado en SQL)
│   │   │
│   │   ├── 📁 registration/       # Entidades: Person, Academy, Competitor
│   │   │   ├── 📁 domain/         # Lógica pura de registro y validación de datos personales
│   │   │   ├── 📁 data/           # Modelos SQLAlchemy y Repositorios (CRUD competidores)
│   │   │   ├── 📁 application/    # Schemas Pydantic (Inscripción de atletas)
│   │   │   └── 📁 api/            # Rutas: /competitors, /academies
│   │   │
│   │   ├── 📁 tournament/         # Entidades: Championship, Category, Modality, Rank
│   │   │   ├── 📁 domain/         # Lógica de categorías (Validación edad/peso)
│   │   │   ├── 📁 data/           # Repositorios (Configuración de campeonatos)
│   │   │   ├── 📁 application/    # Schemas (Filtros de categorías y modalidades)
│   │   │   └── 📁 api/            # Rutas: /championships, /categories
│   │   │
│   │   └── 📁 bracket/            # Entidades: Competitor_Category, Round, Pyramid
│   │       ├── 📁 domain/         # EL CORAZÓN: Algoritmos de generación de llaves (Pirámide)
│   │       ├── 📁 data/           # Persistencia de enfrentamientos y ganadores
│   │       ├── 📁 application/    # Schemas (Representación del árbol de la pirámide)
│   │       └── 📁 api/            # Rutas: /pyramid/generate, /pyramid/winner
│   │
│   └── 📜 main.py                 # Punto de entrada y registro de APIRouters
│
├── 📁 tests/                      <-- TDD: PRUEBAS AUTOMATIZADAS
│   ├── 📁 unit/                   # Tests de dominio (sin base de datos)
│   │   ├── 📜 test_category_logic.py
│   │   └── 📜 test_pyramid_algorithm.py
│   └── 📁 integration/            # Tests de API con base de datos de prueba
│
├── 📜 pyproject.toml              # Dependencias gestionadas por UV
└── 📜 .env                        # Variables de entorno (DB_URL, etc.)