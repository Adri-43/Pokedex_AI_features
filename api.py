from flask import Flask, jsonify, request
try:
    from utils import fetch_data, generate_response, text_to_audio, generate_and_save_image
    from Evolution import get_team_pokemons, evolve_pokemon
    #from MejorEquipo import get_team_details#, get_pokemon_details#, calculate_total_stats
    from Comparador_torneos import get_tournaments, analyze_tournaments
    print("Módulos importados correctamente.")
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    exit(1)

app = Flask(__name__)

BASE_URL = "https://hackeps-poke-backend.azurewebsites.net"

@app.route('/buscar_pokemons/<team_id>', methods=['GET'])
def buscar_pokemons(team_id):
    """
    Busca todos los Pokémon de un equipo específico.
    """
    print(f"Buscando Pokémon para el equipo: {team_id}")
    pokemons = get_team_pokemons(team_id)
    if not pokemons:
        return jsonify({"message": "No Pokémon found for this team."}), 404
    return jsonify(pokemons)

@app.route('/evolucionar/<team_id>', methods=['POST'])
def evolucionar(team_id):
    """
    Evoluciona todos los Pokémon de un equipo.
    """
    print(f"Evolucionando Pokémon para el equipo: {team_id}")
    captured_pokemons = get_team_pokemons(team_id)
    pokemon_groups = {}
    
    for pokemon in captured_pokemons:
        pokemon_id = pokemon["pokemon_id"]
        pokemon_uuid = pokemon["id"]
        
        if pokemon_id not in pokemon_groups:
            pokemon_groups[pokemon_id] = []
        pokemon_groups[pokemon_id].append(pokemon_uuid)
    
    results = []
    for pokemon_id, uuid_list in pokemon_groups.items():
        while len(uuid_list) >= 3:
            pokemon_uuid_list = uuid_list[:3]
            evolve_pokemon(pokemon_uuid_list, team_id)
            uuid_list = uuid_list[3:]
            results.append(f"Pokémon {pokemon_id} evolucionado.")
    
    return jsonify(results)

@app.route('/obtener_descripcion/<pokemon>', methods=['GET'])
def obtener_descripcion(pokemon):
    """
    Obtiene la descripción de un Pokémon.
    """
    print(f"Obteniendo descripción para el Pokémon: {pokemon}")
    messages = [
        {"role": "user", "content": f"""
         You are super friki expert in pokemons so you will give me a 
         description about the following pokemon {pokemon}, you must 
         end with a short funny fact about it, if you dont know the 
         pokemon invent something funny. Give a response in Catalan, 
         no more than 2 paragraphs"""}
    ]
    
    raw_response = generate_response(messages)
    return jsonify({"description": raw_response})

@app.route('/generar_audio', methods=['POST'])
def generar_audio():
    """
    Genera un archivo de audio a partir de una descripción de Pokémon.
    """
    data = request.json
    text = data.get("text")
    filename = data.get("filename", "output_audio.mp3")
    language = data.get("language", "ca")
    
    print(f"Generando audio para el texto: {text}")
    result = text_to_audio(text, filename, language)
    return jsonify({"result": result})

@app.route('/generar_imagen', methods=['POST'])
def generar_imagen():
    """
    Genera una imagen a partir de una descripción de Pokémon.
    """
    data = request.json
    pokemon = data.get("pokemon")  # Obtener el nombre del Pokémon de la solicitud
    filename = data.get("filename", "image_generated.png")

    if not pokemon:
        return jsonify({"error": "El nombre del Pokémon es requerido."}), 400  # Manejo de error si no se proporciona el Pokémon

    # Generar la descripción utilizando el modelo
    messages = [
        {"role": "user", "content": f"""
         You are super friki expert in pokemons so you will give me a 
         description about a picture of the following pokemon {pokemon}
         if you dont know the pokemon invent something funny. 
         Give a response in English"""}
    ]
    
    description = generate_response(messages)  # Generar la descripción
    print(f"Generando imagen para la descripción: {description}")
    
    result = generate_and_save_image(description, filename)  # Usar la descripción generada
    return jsonify({"result": result})

@app.route('/analizar_torneos', methods=['GET'])
def analizar_torneos():
    
    """
    Analiza todos los torneos y determina los resultados de las batallas.
    """
    battles = analyze_tournaments()
    
    # Devolver los resultados de las batallas
    return jsonify(battles)

if __name__ == '__main__':
    print("Iniciando la API...")
    app.run(debug=True) 