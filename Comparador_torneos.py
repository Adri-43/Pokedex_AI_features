import requests
from flask import jsonify
BASE_URL = "https://hackeps-poke-backend.azurewebsites.net"

def get_tournaments():
    """
    Fetches all tournaments using the /tournaments endpoint.
    """
    url = f"{BASE_URL}/tournaments"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Tournaments fetched successfully!")
            return response.json()  # List of tournaments
        else:
            print(f"Failed to fetch tournaments, status code: {response.status_code}")
            print("Response text:", response.text)
            return []
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_team_details(team_id):
    """
    Fetches the details of a team using the /teams/{team_id} endpoint.
    """
    url = f"{BASE_URL}/teams/{team_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Team details
        else:
            print(f"Failed to fetch team details for team ID {team_id}, status code: {response.status_code}")
            return None
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching team details: {e}")
        return None

def get_pokemon_details(pokemon_id):
    """
    Fetches the details of a Pokémon given its ID using the /pokemons/{pokemon_id} endpoint.
    """
    url = f"{BASE_URL}/pokemons/{pokemon_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Pokémon details
        else:
            print(f"Failed to fetch Pokémon details for ID {pokemon_id}, status code: {response.status_code}")
            return None
    
    except requests.RequestException as e:
        print(f"An error occurred while fetching Pokémon details: {e}")
        return None

def calculate_total_stats(pokemon_data):
    """
    Calculate the total stats of a Pokémon, including PS.
    Returns a tuple (total_stats, hp_stat) where:
    - total_stats: the sum of all stats (excluding HP).
    - hp_stat: the value of HP.
    """
    if not pokemon_data:
        return 0, 0  # Return 0 if no data found
    
    # Get the stats from the Pokémon data (base_stat for each stat)
    stats = pokemon_data.get("stats", [])
    
    hp_stat = 0
    total_stats = 0
    
    # Iterate over the stats and accumulate values
    for stat in stats:
        base_stat = stat.get("base_stat", 0)
        stat_name = stat.get("stat", {}).get("name", "")
        
        # Check if the stat is HP and set it separately
        if stat_name == "hp":
            hp_stat = base_stat
        else:
            total_stats += base_stat
    
    return total_stats, hp_stat

def analyze_tournaments():
    """
    Analyzes all tournaments and determines which Pokémon have battled each other,
    including the winner of each battle, by their names and stats.
    """
    tournaments = get_tournaments()
    
    if not tournaments:
        print("No tournaments found.")
        return
    
    battles = []  # Store battle results with names and stats
    
    # Iterate over all tournaments
    for tournament in tournaments:
        tournament_name = tournament.get("name", "Unknown Tournament")
        tournament_combats = tournament.get("tournament_combats", [])
        
        print(f"\nProcessing tournament: {tournament_name} ({len(tournament_combats)} combats)")
        
        # Iterate over each combat in the tournament
        for combat in tournament_combats:
            teams_in_combat = combat.get("teams", [])
            turns = combat.get("turns", [])
            
            # Fetch team details using team IDs
            team1_data = get_team_details(teams_in_combat[0])
            team2_data = get_team_details(teams_in_combat[1])
            
            if not team1_data or not team2_data:
                print(f"Error: Missing team data for teams {teams_in_combat}")
                continue
            
            # Get the captured Pokémon for each team
            team1_pokemons = team1_data.get("captured_pokemons", [])
            team2_pokemons = team2_data.get("captured_pokemons", [])
            
            # Analyze each turn in the combat
            for turn in turns:
                pokemons = turn.get("pokemons", [])
                winner_uuid = turn.get("winner")
                
                if len(pokemons) == 2:
                    pokemon1_uuid = pokemons[0]
                    pokemon2_uuid = pokemons[1]
                    
                    # Get the corresponding Pokémon IDs from the team data
                    pokemon1_id = next((p["pokemon_id"] for p in team1_pokemons if p["id"] == pokemon1_uuid), None)
                    pokemon2_id = next((p["pokemon_id"] for p in team2_pokemons if p["id"] == pokemon2_uuid), None)
                    winner_id = None
                    
                    if winner_uuid in [pokemon1_uuid, pokemon2_uuid]:
                        winner_id = pokemon1_id if winner_uuid == pokemon1_uuid else pokemon2_id
                    
                    # Fetch Pokémon details using their IDs
                    pokemon1_details = get_pokemon_details(pokemon1_id) if pokemon1_id else None
                    pokemon2_details = get_pokemon_details(pokemon2_id) if pokemon2_id else None
                    winner_details = get_pokemon_details(winner_id) if winner_id else None
                    
                    if pokemon1_details and pokemon2_details and winner_details:
                        pokemon1_name = pokemon1_details.get("name", "Unknown")
                        pokemon2_name = pokemon2_details.get("name", "Unknown")
                        winner_name = winner_details.get("name", "Unknown")
                        
                        # Calculate total stats and HP for each Pokémon
                        pokemon1_total_stats, pokemon1_hp = calculate_total_stats(pokemon1_details)
                        pokemon2_total_stats, pokemon2_hp = calculate_total_stats(pokemon2_details)
                        
                        # Add battle result to the list
                        battles.append({
                            "tournament": tournament_name,
                            "pokemon1": pokemon1_name,
                            "pokemon2": pokemon2_name,
                            "pokemon1_stats": pokemon1_total_stats,
                            "pokemon2_stats": pokemon2_total_stats,
                            "pokemon1_hp": pokemon1_hp,
                            "pokemon2_hp": pokemon2_hp,
                            "winner": winner_name
                        })
    
    # Print all battle results
    if battles:
        print("\nBattle Results:")
        for battle in battles:
            print(f"Tournament: {battle['tournament']} | {battle['pokemon1']} (HP: {battle['pokemon1_hp']}, Stats: {battle['pokemon1_stats']}) vs "
                  f"{battle['pokemon2']} (HP: {battle['pokemon2_hp']}, Stats: {battle['pokemon2_stats']}) - Winner: {battle['winner']}")
        return jsonify(battles)
    else:
        print("No battles found.")
        return None

# Run the script
if __name__ == "__main__":
    analyze_tournaments()
