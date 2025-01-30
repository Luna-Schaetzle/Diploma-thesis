import json
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from bert_score import score

# Lade die JSON-Daten
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Berechne BLEU, ROUGE und BERTScore
def calculate_metrics(data):
    results = []
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

    for item in data:
        prompt = item['Prompt']
        response = item['Response']
        reference = item['Reference']

        # BLEU-Score
        bleu_score = sentence_bleu(
            [reference.split()], response.split(), 
            smoothing_function=SmoothingFunction().method4
        )

        # ROUGE-Scores
        rouge_scores = rouge.score(reference, response)

        # BERTScore
        bert_precision, bert_recall, bert_f1 = score(
            [response], [reference], lang="en", verbose=False
        )

        results.append({
            "Prompt": prompt,
            "Response": response,
            "Reference": reference,
            "BLEU": bleu_score,
            "ROUGE-1": rouge_scores['rouge1'].fmeasure,
            "ROUGE-2": rouge_scores['rouge2'].fmeasure,
            "ROUGE-L": rouge_scores['rougeL'].fmeasure,
            "BERTScore-F1": bert_f1.mean().item()
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