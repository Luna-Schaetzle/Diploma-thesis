import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# 1. Lade die Daten (Parquet-Datei)
parquet_file = '/home/luna/.cache/huggingface/hub/datasets--Isotonic--human_assistant_conversation/snapshots/eefe292fe4eec3bcc82a59c662bb8380510356cf/data/validation-00000-of-00001-97966736f3498654.parquet'
df = pd.read_parquet(parquet_file)

# 2. Erstelle ein Dataset aus der Pandas DataFrame
ds = Dataset.from_pandas(df)

# 3. Lade das Modell und den Tokenizer
model_name = "meta-llama/llama-3.2-1b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Setze das Pad-Token auf das EOS-Token
tokenizer.pad_token = tokenizer.eos_token

# 4. Tokenisierung der Daten
def tokenize_function(examples):
    # Tokenisiere die Eingabe und das Antwortpaar
    inputs = tokenizer(examples['prompt'], truncation=True, padding="max_length", max_length=512)
    targets = tokenizer(examples['response'], truncation=True, padding="max_length", max_length=512)

    # Labels setzen: Das Modell soll den nächsten Token der Antwort vorhersagen
    inputs['labels'] = targets['input_ids']
    return inputs

# Wende die Tokenisierung auf das Dataset an
tokenized_datasets = ds.map(tokenize_function, batched=True)

# 5. Aufteilen der Daten in Training und Validierung (80% Training, 20% Validierung)
train_dataset = tokenized_datasets.train_test_split(test_size=0.2)["train"]
eval_dataset = tokenized_datasets.train_test_split(test_size=0.2)["test"]

# 6. Definiere die Trainingsargumente
training_args = TrainingArguments(
    output_dir="./results",          # Speichert die Modell-Checkpoints
    evaluation_strategy="epoch",     # Evaluation nach jeder Epoche
    learning_rate=2e-5,              # Lernrate
    per_device_train_batch_size=4,   # Batch-Größe pro Gerät (kann je nach GPU angepasst werden)
    num_train_epochs=3,              # Anzahl der Trainingsepochen
    weight_decay=0.01,               # Gewichtung der Regularisierung
    save_strategy="epoch",          # Speichern des Modells nach jeder Epoche
    logging_dir="./logs",            # Logs speichern
    logging_steps=10,                # Logging nach 10 Schritten
)

# 7. Trainer initialisieren
trainer = Trainer(
    model=model,                     # Das Modell, das trainiert wird
    args=training_args,              # Trainingsargumente
    train_dataset=train_dataset,     # Trainingsdaten
    eval_dataset=eval_dataset,       # Validierungsdaten
)

# 8. Training starten
trainer.train()

# 9. Modell speichern
model.save_pretrained("./final_model")
tokenizer.save_pretrained("./final_model")

# 10. Evaluierung des Modells
results = trainer.evaluate()
print(results)