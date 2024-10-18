import pandas as pd
from datasets import Dataset

# Lade die Parquet-Datei, die du bereits benutzt hast
parquet_file = '/home/luna/.cache/huggingface/hub/datasets--Isotonic--human_assistant_conversation/snapshots/eefe292fe4eec3bcc82a59c662bb8380510356cf/data/validation-00000-of-00001-97966736f3498654.parquet'
df = pd.read_parquet(parquet_file)

# Überprüfe die ersten paar Zeilen des DataFrames
print(df.head())

# Umbenennen der Spalten und Umwandeln in ein Dataset
def rename_columns(example):
    example['prompt'] = example['prompt']  # Behalte die 'prompt'-Spalte bei
    example['response'] = example['response']  # Behalte die 'response'-Spalte bei
    example['text'] = example['source_text']  # Umbenennen der 'source_text'-Spalte in 'text'
    return example

# Umwandeln des Pandas DataFrames in ein Huggingface Dataset
ds = Dataset.from_pandas(df)

# Wende die Umbenennung der Spalten an
ds = ds.map(rename_columns)

# Überprüfe die Struktur des Datasets
print(ds.features)
