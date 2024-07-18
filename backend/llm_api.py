import requests
from typing import Dict, Any

LLM_API_URL = "https://api.example.com/llm"  # Sostituisci con l'URL effettivo dell'API
API_KEY = "your_api_key_here"  # Sostituisci con la tua chiave API

def call_llm_api(text: str, schema: Dict[str, str]) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "schema": schema
    }
    
    try:
        response = requests.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Errore nella chiamata all'API LLM: {e}")
        return {}

# Esempio di utilizzo
if __name__ == "__main__":
    sample_text = "Questo è un testo di esempio."
    sample_schema = {
        "nome": "Nome della persona",
        "età": "Età della persona",
        "occupazione": "Lavoro della persona"
    }
    
    result = call_llm_api(sample_text, sample_schema)
    print("Risultato dell'API LLM:", result)