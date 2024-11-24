# Proyecto de API Pokémon

Este proyecto es una API para interactuar con datos de Pokémon, permitiendo realizar diversas operaciones como buscar Pokémon, obtener descripciones, evolucionar Pokémon y analizar torneos.

## Requisitos

- Python 3.x
- pip

## Instalación

1. **Crea un entorno virtual:**

   ```bash
   python -m venv env_duck
   ```

2. **Activa el entorno virtual:**

   - En Windows:
     ```bash
     env_duck\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env_duck/bin/activate
     ```

3. **Instala las dependencias:**

   ```bash
   pip install -U g4f[all]
   pip install -r requirements.txt
   ```

## Ejecución de la API

Para iniciar la API, ejecuta el siguiente comando:

```bash
python api.py
```

La API se ejecutará en `http://127.0.0.1:5000`.

## Pruebas

Puedes ejecutar las pruebas de la API utilizando el siguiente comando:

```bash
python test_api.py
```

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.