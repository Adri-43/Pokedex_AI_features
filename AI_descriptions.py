from utils import generate_response, text_to_audio, generate_and_save_image

pokemon = "Pikachu"
messages = [
    {"role": "user", "content": f"""
     You are super friki expert in pokemons so you will give me a 
     description about the following pokemon {pokemon}, you must 
     end with a short funny fact about it, if you dont know the 
     pokemon invent something funny. Give a response in Catalan, 
     no more than 2 parragraphs"""}
]

raw_response = generate_response(messages)
print(raw_response)

result = text_to_audio(raw_response, filename=f"audios/description_{pokemon}.mp3", language="ca")
print(result)

messages = [
    {"role": "user", "content": f"""
     You are super friki expert in pokemons so you will give me a 
     description about a picture of the following pokemon {pokemon}
     if you dont know the pokemon invent something funny. 
     Give a response in English"""}
]

description = generate_response(messages)
print(description)

generate_and_save_image(description, filename=f"image_{pokemon}.png")
