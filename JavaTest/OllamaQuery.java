import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class OllamaQuery {
    
    public static String queryOllama(String model, String prompt) throws Exception {
        String urlString = "http://localhost:11434/v1/completions";
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        // JSON-Payload vorbereiten
        String payload = String.format("{\"model\": \"%s\", \"prompt\": \"%s\"}", model, prompt);

        // Anfrage senden
        OutputStream os = conn.getOutputStream();
        OutputStreamWriter writer = new OutputStreamWriter(os, "UTF-8");
        writer.write(payload);
        writer.flush();
        writer.close();
        os.close();

        // Antwortcode prüfen
        int responseCode = conn.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            Scanner responseScanner = new Scanner(conn.getInputStream(), "UTF-8");
            StringBuilder responseBuilder = new StringBuilder();
            while (responseScanner.hasNextLine()) {
                responseBuilder.append(responseScanner.nextLine());
            }
            responseScanner.close();
            String response = responseBuilder.toString();

            // Text aus der Antwort extrahieren
            if (response.contains("choices")) {
                int textStart = response.indexOf("\"text\":") + 8;
                int textEnd = response.indexOf("\"", textStart);
                return response.substring(textStart, textEnd);
            } else {
                return "Error: No text found in response.";
            }
        } else {
            return "Error: " + responseCode + " - " + conn.getResponseMessage();
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("You: ");
            String question = scanner.nextLine();
            if (question.equals("exit")) {
                break;
            }

            // Anfrage an Ollama senden
            try {
                String result = queryOllama("llama3.1", question);
                System.out.println("Ollama: " + result);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        scanner.close();
    }
}
