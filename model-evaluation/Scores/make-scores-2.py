import json
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import language_tool_python
import textstat
from transformers import pipeline, logging

# Unterdrücke Transformer-Warnungen
logging.set_verbosity_error()

# Lade die JSON-Daten
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Berechne BLEU, ROUGE, Grammatikalische Korrektheit, Lesbarkeit und Sentiment
def calculate_metrics(data):
    results = []
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    grammar_tool = language_tool_python.LanguageTool('en-US')
    sentiment_analyzer = pipeline(
        'sentiment-analysis', 
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
        max_length=512
    )

    for item in data:
        prompt = item['Prompt']
        response = item['Response']
        reference = item['Reference']

        try:
            # BLEU-Score
            bleu_score = sentence_bleu(
                [reference.split()], response.split(), 
                smoothing_function=SmoothingFunction().method4
            )

            # ROUGE-Scores
            rouge_scores = rouge.score(reference, response)

            # Grammar Check
            grammar_errors = len(grammar_tool.check(response))

            # Readability Score
            readability_score = textstat.flesch_reading_ease(response)

            # Sentiment Analysis
            # Sentiment Analysis mit Fehlerbehandlung
            try:
                sentiment_result = sentiment_analyzer(response)[0]
                sentiment = sentiment_result['label']
            except Exception as e:
                print(f"Sentiment error for prompt '{prompt}': {e}")
                sentiment = "Error"

            results.append({
                "Prompt": prompt,
                "Response": response,
                "Reference": reference,
                "BLEU": bleu_score,
                "ROUGE-1": rouge_scores['rouge1'].fmeasure,
                "ROUGE-2": rouge_scores['rouge2'].fmeasure,
                "ROUGE-L": rouge_scores['rougeL'].fmeasure,
                "Grammar Errors": grammar_errors,
                "Readability Score": readability_score,
                "Sentiment": sentiment
            })
        except Exception as e:
            print(f"Error processing prompt '{prompt}': {e}")
            results.append({
                "Prompt": prompt,
                "Response": response,
                "Reference": reference,
                "Error": str(e)
            })

    return results

# Speichere die Ergebnisse in einer neuen JSON-Datei
def save_results(results, output_path):
    with open(output_path, 'w') as file:
        json.dump(results, file, indent=4)

# Hauptfunktion
def main():
    directory = input("Enter the directory containing the processed JSON files: ")

    try:
        for file_name in os.listdir(directory):
            if file_name.startswith("processed_") and file_name.endswith(".json"):
                input_file = os.path.join(directory, file_name)
                model_name = file_name.split("processed_")[1].split(".json")[0]
                output_file = os.path.join(directory, f"scored_{model_name}.json")

                print(f"Processing file: {input_file}")
                data = load_json(input_file)
                metrics = calculate_metrics(data)
                save_results(metrics, output_file)
                print(f"Metrics saved to: {output_file}")

    except FileNotFoundError:
        print(f"Error: The directory {directory} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
