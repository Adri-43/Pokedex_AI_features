import requests
import unittest

BASE_URL = "http://127.0.0.1:5000"

class TestAPI(unittest.TestCase):

    '''def test_buscar_pokemons(self):
        team_id = "ba562df3-da75-44c1-902e-1a551a92684a"
        response = requests.get(f"{BASE_URL}/buscar_pokemons/{team_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)  # Asegúrate de que la respuesta sea una lista
    '''
    def test_mejor_equipo(self):
        team_id = "ba562df3-da75-44c1-902e-1a551a92684a"
        response = requests.get(f"{BASE_URL}/mejor_equipo/{team_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json())  # Asegúrate de que la respuesta contenga el nombre del mejor Pokémon

    def test_evolucionar(self):
        team_id = "ba562df3-da75-44c1-902e-1a551a92684a"
        response = requests.post(f"{BASE_URL}/evolucionar/{team_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)  # Asegúrate de que la respuesta sea una lista de resultados

    def test_obtener_descripcion(self):
        pokemon = "Dialga"
        response = requests.get(f"{BASE_URL}/obtener_descripcion/{pokemon}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("description", response.json())  # Asegúrate de que la respuesta contenga la descripción

    def test_generar_audio(self):
        response = requests.post(f"{BASE_URL}/generar_audio", json={
            "text": "This is a test description.",
            "filename": "test_audio.mp3",
            "language": "ca"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())  # Asegúrate de que la respuesta contenga el resultado

    def test_generar_imagen(self):
        response = requests.post(f"{BASE_URL}/generar_imagen", json={
            "description": "This is a test description for an image.",
            "filename": "test_image.png"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())  # Asegúrate de que la respuesta contenga el resultado

if __name__ == "__main__":
    unittest.main() 