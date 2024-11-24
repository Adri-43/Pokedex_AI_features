# Documentación de la API Pokémon

Esta documentación describe los endpoints disponibles en la API Pokémon y cómo interactuar con ellos.

## Base URL

La API se ejecuta en la siguiente URL base:

http://127.0.0.1:5000

## Endpoints

### 1. Buscar Pokémon

- **URL:** `/buscar_pokemons/<team_id>`
- **Método:** `GET`
- **Descripción:** Busca todos los Pokémon de un equipo específico.
- **Parámetros:**
  - `team_id`: ID del equipo.
- **Respuesta:**
  - `200 OK`: Devuelve una lista de Pokémon.
  - `404 Not Found`: Si no se encuentran Pokémon.

### 2. Obtener el Mejor Pokémon

- **URL:** `/mejor_equipo/<team_id>`
- **Método:** `GET`
- **Descripción:** Obtiene el mejor Pokémon del equipo basado en estadísticas.
- **Parámetros:**
  - `team_id`: ID del equipo.
- **Respuesta:**
  - `200 OK`: Devuelve el mejor Pokémon.
  - `404 Not Found`: Si no se encuentra el equipo.

### 3. Evolucionar Pokémon

- **URL:** `/evolucionar/<team_id>`
- **Método:** `POST`
- **Descripción:** Evoluciona todos los Pokémon de un equipo.
- **Parámetros:**
  - `team_id`: ID del equipo.
- **Respuesta:**
  - `200 OK`: Devuelve una lista de resultados de evolución.

### 4. Obtener Descripción de un Pokémon

- **URL:** `/obtener_descripcion/<pokemon>`
- **Método:** `GET`
- **Descripción:** Obtiene la descripción de un Pokémon.
- **Parámetros:**
  - `pokemon`: Nombre del Pokémon.
- **Respuesta:**
  - `200 OK`: Devuelve la descripción del Pokémon.

### 5. Generar Audio

- **URL:** `/generar_audio`
- **Método:** `POST`
- **Descripción:** Genera un archivo de audio a partir de una descripción de Pokémon.
- **Cuerpo de la Solicitud:**
  ```json
  {
      "text": "Texto a convertir en audio",
      "filename": "nombre_del_archivo.mp3",
      "language": "ca"
  }
  ```
- **Respuesta:**
  - `200 OK`: Devuelve el resultado de la generación de audio.

### 6. Generar Imagen

- **URL:** `/generar_imagen`
- **Método:** `POST`
- **Descripción:** Genera una imagen a partir de una descripción de Pokémon.
- **Cuerpo de la Solicitud:**
  ```json
  {
      "description": "Descripción para generar la imagen",
      "filename": "nombre_de_la_imagen.png"
  }
  ```
- **Respuesta:**
  - `200 OK`: Devuelve el resultado de la generación de la imagen.

### 7. Analizar Torneos

- **URL:** `/analizar_torneos`
- **Método:** `GET`
- **Descripción:** Analiza todos los torneos y determina los resultados de las batallas.
- **Respuesta:**
  - `200 OK`: Devuelve los resultados de las batallas.
  - `404 Not Found`: Si no se encuentran torneos.

## Ejemplo de Uso

Para buscar Pokémon de un equipo, puedes hacer una solicitud GET a:

GET http://127.0.0.1:5000/buscar_pokemons/ba562df3-da75-44c1-902e-1a551a92684a

## Conclusión

Esta API proporciona una forma sencilla de interactuar con datos de Pokémon. Si tienes preguntas o necesitas ayuda, no dudes en abrir un issue en el repositorio.