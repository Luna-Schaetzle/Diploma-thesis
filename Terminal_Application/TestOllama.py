import requests

def query_ollama(model: str, prompt: str):
    url = "http://localhost:11434/v1/completions"  # API-Endpunkt von Ollama
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt
    }

    # Anfrage senden
    response = requests.post(url, json=payload, headers=headers)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        response_json = response.json()
        # Das generierte Ergebnis befindet sich in choices[0]["text"]
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["text"]
        else:
            return "Error: No text found in response."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Beispiel: Anfrage an das Modell 'llama3.1'
result = query_ollama("llama3.1", "What is the capital of Germany?")
print(result)
