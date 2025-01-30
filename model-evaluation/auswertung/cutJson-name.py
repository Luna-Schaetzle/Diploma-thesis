import os
import glob

def clean_filename(filename):
    """Entfernt unerwünschte Suffixe aus Dateinamen"""
    suffixes = [
        '_response_time_results_ressours_usage',
        '_response_time_results',
        '_ressours_usage'
    ]
    
    base_name = os.path.splitext(filename)[0]
    
    for suffix in suffixes:
        if base_name.endswith(suffix):
            new_base = base_name[:-len(suffix)]
            return f"{new_base}.json"
    
    return filename

def rename_files():
    """Benennt Dateien um und vermeidet Überschreibungen"""
    files = glob.glob("*_response_time_results_ressours_usage.json")
    counter = 1
    
    for old_file in files:
        new_file = clean_filename(old_file)
        
        # Vermeide Namenskonflikte
        while os.path.exists(new_file) and new_file != old_file:
            new_file = f"{os.path.splitext(new_file)[0]}_{counter}.json"
            counter += 1
        
        try:
            os.rename(old_file, new_file)
            print(f"Umbenannt: {old_file} -> {new_file}")
        except Exception as e:
            print(f"Fehler bei {old_file}: {str(e)}")

def main():
    print("Starte Umbenennungsprozess...")
    rename_files()
    print("\nÜberblick der neuen Dateinamen:")
    for f in glob.glob("*.json"):
        print(f" - {f}")

if __name__ == "__main__":
    main()