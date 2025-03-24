import matplotlib.pyplot as plt

# Daten
personen = ["Luna", "Alle (oL)", "Gabriel", "Flo"]
stunden = [103.00, 8.00, 19.05, 82.48]

# Diagramm erstellen
plt.figure(figsize=(8, 5))
plt.bar(personen, stunden, color=["blue", "gray", "green", "red"])

# Titel und Achsenbeschriftung
plt.title("Arbeitsstundenübersicht")
plt.xlabel("Personen")
plt.ylabel("Stunden")
plt.ylim(0, max(stunden) + 10)

# Werte auf den Balken anzeigen
for i, v in enumerate(stunden):
    plt.text(i, v + 2, str(v), ha='center', fontsize=12)

# Diagramm anzeigen
plt.show()
