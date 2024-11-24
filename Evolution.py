from utils import fetch_data
import requests
BASE_URL = "https://hackeps-poke-backend.azurewebsites.net"

def get_team_pokemons(team_id):
    """
    Fetches all Pokémon from a specific team using the /teams/{team_id} endpoint.
    """
    url = f"{BASE_URL}/teams/{team_id}"
    headers = {"Content-Type": "application/json"}
    team_data = fetch_data(url, headers)
    if team_data:
        print("Pokémon list from team fetched successfully!")
        return team_data.get("captured_pokemons", [])
    return []

def get_pokemon_name(pokemon_id):
    """
    Fetches the name of a Pokémon given its ID using the /pokemons/{pokemon_id} endpoint.
    """
    url = f"{BASE_URL}/pokemons/{pokemon_id}"
    headers = {"Content-Type": "application/json"}
    pokemon_data = fetch_data(url, headers)
    if pokemon_data:
        return pokemon_data.get("name", "Unknown")
    return "Unknown"

def evolve_pokemon(pokemon_uuid_list, team_id):
    """
    Evolves a Pokémon using the /pokemons/{pokemon_id}/evolve endpoint.
    Requires 3 UUIDs of the same Pokémon.
    """
    url = f"{BASE_URL}/pokemons/{pokemon_uuid_list[0]}/evolve"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "pokemon_uuid_list": pokemon_uuid_list,
        "team_id": team_id
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Pokémon with UUIDs {pokemon_uuid_list} evolved successfully!")
        else:
            print(f"Failed to evolve Pokémon, Status code: {response.status_code}")
            print("Response text:", response.text)
    
    except requests.RequestException as e:
        print(f"An error occurred while evolving Pokémon: {e}")

def main():
    """
    Main function to handle fetching Pokémon from the team, counting them, and evolving those with 3 or more.
    """
    team_id = "ba562df3-da75-44c1-902e-1a551a92684a"
    
    # Fetch all Pokémon in the team
    captured_pokemons = get_team_pokemons(team_id)
    
    # If no Pokémon were found, exit
    if not captured_pokemons:
        print("No Pokémon found in the team.")
        return
    
    # Count the occurrences of each pokemon_id and group their UUIDs
    pokemon_groups = {}
    for pokemon in captured_pokemons:
        pokemon_id = pokemon["pokemon_id"]
        pokemon_uuid = pokemon["id"]
        
        if pokemon_id not in pokemon_groups:
            pokemon_groups[pokemon_id] = []
        pokemon_groups[pokemon_id].append(pokemon_uuid)
    
    # Attempt to evolve all Pokémon with 3 or more UUIDs
    for pokemon_id, uuid_list in pokemon_groups.items():
        pokemon_name = get_pokemon_name(pokemon_id)
        
        print(f"Processing Pokémon: {pokemon_name} (ID: {pokemon_id}), Total: {len(uuid_list)}")
        
        while len(uuid_list) >= 3:
            pokemon_uuid_list = uuid_list[:3]
            evolve_pokemon(pokemon_uuid_list, team_id)
            uuid_list = uuid_list[3:]
    
    print("All evolutions processed!")

# Run the script
if __name__ == "__main__":
    main()
