import os
from dotenv import load_dotenv

load_dotenv()

USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def ask_gemini(prompt):
    if USE_OLLAMA:
        return ask_ollama(prompt)
    if USE_OPENAI:
        return ask_openai(prompt)
    
    from google import genai
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def ask_ollama(prompt):
    import requests
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        return response.json().get("response", "No response from Ollama")
    except Exception as e:
        return f"Ollama error: {str(e)}"

def ask_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content