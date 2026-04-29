from google import genai

client = genai.Client(api_key="AIzaSyClI-f0Bk2kTmSpPQG3Uej0PNpAURdESms")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hola, responde solo OK"
)

print(response.text)