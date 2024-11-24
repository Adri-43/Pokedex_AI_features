from utils import fetch_data

BASE_URL = "https://hackeps-poke-backend.azurewebsites.net"

def get_team_details(team_id):
    """
    Fetches the details of a team using the /teams/{team_id} endpoint.
    """
    url = f"{BASE_URL}/teams/{team_id}"
    headers = {"Content-Type": "application/json"}
    return fetch_data(url, headers)

def get_pokemon_details(pokemon_id):
    """
    Fetches the details of a Pokémon given its ID using the /pokemons/{pokemon_id} endpoint.
    """
    url = f"{BASE_URL}/pokemons/{pokemon_id}"
    headers = {"Content-Type": "application/json"}
    return fetch_data(url, headers)

def calculate_total_stats(pokemon_data):
    """
    Calculate the total stats of a Pokémon, including HP.
    Returns a tuple (total_stats, hp_stat) where:
    - total_stats: the sum of all stats (excluding HP).
    - hp_stat: the value of HP.
    """
    if not pokemon_data:
        return 0, 0  # Return 0 if no data found
    
    stats = pokemon_data.get("stats", [])
    hp_stat = 0
    total_stats = 0
    
    for stat in stats:
        base_stat = stat.get("base_stat", 0)
        stat_name = stat.get("stat", {}).get("name", "")
        
        if stat_name == "hp":
            hp_stat = base_stat
        else:
            total_stats += base_stat
    
    return total_stats, hp_stat

def get_best_pokemon_for_team(team_id):
    """
    Gets the top 6 Pokémon from the team based on stats and HP, showing only the best Pokémon.
    """
    team_data = get_team_details(team_id)
    
    if not team_data:
        print("Failed to fetch team data.")
        return None
    
    team_pokemons = team_data.get("captured_pokemons", [])
    
    if not team_pokemons:
        print("No captured Pokémon found in this team.")
        return None
    
    pokemon_stats = []
    
    for pokemon in team_pokemons:
        pokemon_uuid = pokemon.get("id")
        pokemon_id = pokemon.get("pokemon_id")
        
        pokemon_details = get_pokemon_details(pokemon_id)
        
        if pokemon_details:
            total_stats, hp_stat = calculate_total_stats(pokemon_details)
            pokemon_stats.append({
                "uuid": pokemon_uuid,
                "name": pokemon_details.get("name", "Unknown"),
                "id": pokemon_id,
                "hp": hp_stat,
                "total_stats": total_stats
            })
    
    sorted_pokemons = sorted(pokemon_stats, key=lambda x: (x["total_stats"], x["hp"]), reverse=True)
    
    print(f"Top 6 Pokémon for team {team_id}:")
    for i, pokemon_data in enumerate(sorted_pokemons[:6]):
        print(f"{i+1}. Name: {pokemon_data['name']} | ID: {pokemon_data['id']} | UUID: {pokemon_data['uuid']} | HP: {pokemon_data['hp']} | Total Stats: {pokemon_data['total_stats']}")

# Team ID to evaluate
team_id = "ba562df3-da75-44c1-902e-1a551a92684a"

# Run the function to get the best Pokémon for the team
get_best_pokemon_for_team(team_id)
