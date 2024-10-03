document.getElementById('ollamaButton').addEventListener('click', function() {
    // API-Endpoint von Ollama (dieser müsste durch den tatsächlichen API-Endpoint ersetzt werden)
    const url = 'https://api.ollama.ai/endpoint';  // Beispiel-URL

    // Die Daten, die an Ollama gesendet werden
    const data = {
        query: "Was ist AI?",
        model: "llama3.2:1b" // Beispiel-Parameter
    };

    // Sendet eine POST-Anfrage an Ollama
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Ausgabe der Antwort von Ollama
        document.getElementById('response').innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => {
        console.error('Fehler:', error);
    });
});
