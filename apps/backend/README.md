## 🚀 Inicio Rápido (Desarrollo)

### Pasos para levantar el Backend
1.  Clona el repositorio: `git clone <tu-repo-url>`
2.  Abre la carpeta raíz en VS Code.
3.  Presiona `F1` y selecciona: **"Dev Containers: Reopen in Container"**.
4.  Una vez dentro del contenedor, el entorno de Python se sincronizará automáticamente.

---

## 🛠️ Herramientas de Backend

El backend utiliza **`uv`** para una gestión de paquetes ultra rápida.

* **Sincronizar dependencias:** `uv sync`
* **Ejecutar pruebas (TDD):** `uv run pytest`
* **Iniciar API en modo desarrollo:** ```bash
    cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
* **Documentación Interactiva:** Una vez iniciada, visita `http://localhost:8000/docs`

---

## 📐 Principios de Diseño

1.  **DDD (Domain-Driven Design):** La lógica de emparejamientos reside en el corazón del dominio, protegida de cambios en la base de datos o el framework web.
2.  **TDD (Test-Driven Development):** Cada regla de la pirámide (por ejemplo: "un jugador no puede jugar contra sí mismo") está respaldada por una prueba unitaria.
3.  **CamelCase Integration:** La API se comunica en `camelCase` para una integración nativa con el frontend en TypeScript, mientras mantiene el estándar `snake_case` de Python internamente.

---

## 📜 Guías Específicas
Para más detalles sobre las reglas de desarrollo del backend, consulta el archivo:
👉 [`backend/agent.md`](./backend/agent.md)