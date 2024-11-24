from g4f.client import Client, Images
import requests
from gtts import gTTS

client = Client()

def generate_response(system_message):
    """
    Genera una respuesta utilizando el modelo GPT-4o.

    Args:
        system_message (list): Lista de mensajes para el modelo.

    Returns:
        str: Contenido de la respuesta generada.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        provider="Blackbox",
        messages=system_message
    )
    return response.choices[0].message.content

def text_to_audio(text, filename="output_audio.mp3", language="en"):
    """
    Convierte texto a un archivo de audio.

    Args:
        text (str): El texto que se convertirá en audio.
        filename (str): El nombre del archivo de salida (por defecto: 'output_audio.mp3').
        language (str): El idioma del texto (por defecto: 'en' para inglés).
    
    Returns:
        str: Mensaje indicando si el audio se guardó correctamente o hubo un error.
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        return f"Audio guardado como '{filename}'"
    except Exception as e:
        return f"Error al generar el audio: {e}"

def generate_and_save_image(description, filename="image_generated.png"):
    """
    Genera y guarda una imagen a partir de una descripción.

    Args:
        description (str): Descripción para generar la imagen.
        filename (str): Nombre del archivo de imagen a guardar (por defecto: 'image_generated.png').
    
    Returns:
        str: Mensaje indicando si la imagen se guardó correctamente o hubo un error.
    """
    try:
        response = client.images.generate(prompt=description, model="flux-anime", response_format="url")
        image_url = response.data[0].url

        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(img_response.content)
            return f"Imagen guardada como '{filename}'"
        return "Error al descargar la imagen"
    except Exception as e:
        return f"Error: {e}"

def fetch_data(url, headers):
    """
    Realiza una solicitud GET a la URL proporcionada y devuelve los datos en formato JSON.

    Args:
        url (str): URL para realizar la solicitud.
        headers (dict): Encabezados para la solicitud.

    Returns:
        dict: Datos en formato JSON si la solicitud es exitosa, None en caso contrario.
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al realizar la solicitud, código de estado: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Ocurrió un error: {e}")
        return None

def send_post_request(zone_id, team_id):
    """
    Envía una solicitud POST a una zona específica con el team_id proporcionado.

    Args:
        zone_id (str): ID de la zona a la que se enviará la solicitud.
        team_id (str): ID del equipo que se enviará en la solicitud.
    """
    base_url = f"https://hackeps-poke-backend.azurewebsites.net/events/{zone_id}"
    payload = {"team_id": team_id}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(base_url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Solicitud a la zona {zone_id} exitosa!")
            print("Respuesta:", response.json())
        else:
            print(f"Solicitud a la zona {zone_id} fallida con código de estado {response.status_code}")
            print("Error:", response.text)
    except requests.RequestException as e:
        print(f"Ocurrió un error al solicitar la zona {zone_id}:", e)
