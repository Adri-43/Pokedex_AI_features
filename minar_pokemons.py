import requests
import time

API_URL_LOCAL = "http://127.0.0.1:5000"  # URL de la API local
API_URL_REMOTE = "https://hackeps-poke-backend.azurewebsites.net"  # URL de la API remota

def main():
    """
    Función principal para manejar las solicitudes POST con cooldown por zona.
    """
    # Diccionario de zonas con su cooldown (en segundos)
    zones_cooldown = {
        "6737278e28aebf267e089bec": 7220,
        "67372c23ea45b856683249f4": 7220,
        "67372c31f895d5d1b4d6c2a9": 1820,
        "6710c41ed814fc8dae914171": 20020,
        "67372c2a2219842167aa3e0c": 3620,
        "67372c4a591a6cbabccfc012": 2020,
        "67372c1c7a5c6e90024299e1": 7220,
        "67372c56ec018d7dedd34ee3": 4820,
        "67372c39c499cd12be6bef9e": 4820,
        "67372c686fa2f2902a4b7c2a": 4820,
        "67372c61f269e28d2f86f063": 3620,
        "67372c44db061db993104ce1": 7020
    }
    
    # Inicializa un diccionario para registrar el último tiempo de ejecución de cada zona
    last_execution_time = {zone_id: 0 for zone_id in zones_cooldown}
    
    # ID del equipo para las solicitudes
    team_id = "ba562df3-da75-44c1-902e-1a551a92684a"  # Reemplaza con tu team ID

    # Bucle principal
    while True:
        current_time = time.time()  # Obtiene el tiempo actual en segundos
        for zone_id, cooldown in zones_cooldown.items():
            # Verifica si ha pasado el cooldown para esta zona
            if current_time - last_execution_time[zone_id] > cooldown:
                print(f"Enviando solicitud a la zona {zone_id}...")
                
                # Realiza la solicitud POST a la API remota
                payload = {"team_id": team_id}
                response = requests.post(f"{API_URL_REMOTE}/events/{zone_id}", json=payload)
                
                if response.status_code == 200:
                    print(f"Respuesta de la zona {zone_id}: {response.json()}")
                    # Actualiza el tiempo de la última ejecución
                    last_execution_time[zone_id] = current_time
                else:
                    print(f"Error al solicitar la zona {zone_id}, código de estado: {response.status_code}")

        # Espera un tiempo antes de revisar nuevamente (puedes ajustarlo según sea necesario)
        time.sleep(1)

# Punto de entrada del script
if __name__ == "__main__":
    main()
