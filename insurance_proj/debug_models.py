import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    print("Listing models...")
    # The method to list models might be client.models.list()
    # It returns an iterator.
    for m in client.models.list():
        print(f"Model: {m.name}")
        print(f"  Supported generation methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")

try:
    print("\nAttempting to generate content with 'gemini-1.5-flash'...")
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello"
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error generating content: {e}")
