import speech_recognition as sr
from translate import Translator
from monsterapi import client
import requests
from PIL import Image

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE5NzMxNmZhZmY4NTFjYjVhNzdhYmNjZjA2MGE5MmI0IiwiY3JlYXRlZF9hdCI6IjIwMjUtMDItMTNUMTY6Mzk6NDguNTM3ODU0In0._dTFa25L5UMATIr7vMipwjndu7OB6VgxohwEeQgpdas'  # Replace 'your-api-key' with your actual Monster API key
monster_client = client(api_key)

recognizer = sr.Recognizer()
translate = Translator(from_lang="hi", to_lang="en")  # Correct instantiation

with sr.Microphone() as source:
    print("Say something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="hi-IN")
    
    translated_text = translate.translate(text)  # Correct call: translate.translate(text)
    print(translated_text)
except sr.UnknownValueError:
    print("can't understand")
except sr.RequestError:
    print("google API Error")

model = 'txt2img'  # Replace with the desired model name
input_data = {
'prompt': f'{translated_text}',
'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
'samples': 1,
'steps': 50,
'aspect_ratio': 'square',
'guidance_scale': 7.5,
'seed': 2414,
            }

print("Generating....")
result = monster_client.generate(model, input_data)

img_url = result['output'][0]

file_name = 'image.png'

responce = requests.get(img_url)
if responce.status_code == 200:
    with open(file_name,'wb') as file:
        file.write(responce.content)
        print("image downloaded")

        img = Image.open(file_name)
        img.show()
else:
    print("failed")