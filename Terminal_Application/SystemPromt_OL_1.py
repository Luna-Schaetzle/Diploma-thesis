import requests

def query_ollama_with_system_prompt(model: str, system_prompt: str, user_prompt: str):
    url = "http://localhost:11434/v1/completions"  # API-Endpunkt von Ollama
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "system_prompt": system_prompt,  # Der System-Prompt für das Modell
        "prompt": user_prompt  # Der User-Prompt oder die Frage
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

# Beispiel: Anfrage mit einem System-Prompt
system_prompt = "You are SAIPiA, a self-sufficient AI assistant designed to run on limited hardware (Raspberry Pi). Your main functions include processing requests efficiently, retrieving data from local databases, recognizing speech and images, and generating concise and accurate responses. You should prioritize the optimal use of resources, providing real-time updates when tasks take longer to complete. Your communication should be polite, clear, and informative, offering the user useful guidance or explanations when needed, while ensuring a smooth and responsive experience."
user_prompt = "/show system"

result = query_ollama_with_system_prompt("llama3.1", system_prompt, user_prompt)
print(result)
