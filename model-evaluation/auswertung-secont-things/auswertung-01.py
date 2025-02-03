import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Daten aggregieren
directory = "./"
all_data = []
for file in os.listdir(directory):
    if file.startswith("scored_") and file.endswith(".json"):
        model = file.replace("scored_", "").replace(".json", "")
        df = pd.read_json(os.path.join(directory, file))
        df["Model"] = model
        all_data.append(df)
df = pd.concat(all_data)

# Gemeinsame Style-Einstellungen
sns.set_theme(style="whitegrid", font_scale=0.9)
plt.rcParams['axes.titlepad'] = 15
plt.rcParams['axes.labelpad'] = 10

def rotate_labels(ax, rotation=45, ha='right'):
    """Rotiert x-Achsen Labels und passt Ausrichtung an"""
    ax.set_xticklabels(ax.get_xticklabels(), 
                      rotation=rotation, 
                      ha=ha,
                      fontsize=9)
    plt.tight_layout()

# 1. BLEU & ROUGE Scores
plt.figure(figsize=(14, 7))
df_melt = df.melt(id_vars=["Model"], value_vars=["BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L"], 
                  var_name="Metric", value_name="Score")
ax = sns.barplot(x="Model", y="Score", hue="Metric", data=df_melt, palette="viridis")
plt.title("Vergleich von BLEU und ROUGE Scores", fontweight='bold')
plt.ylim(0, 0.05)
plt.legend(loc="upper right", frameon=True)
rotate_labels(ax)
plt.savefig("bleu_rouge.png", dpi=300, bbox_inches="tight")

# 2. Grammatikalische Fehler
plt.figure(figsize=(12, 6))
ax = sns.boxplot(x="Model", y="Grammar Errors", data=df, palette="Set2")
plt.title("Verteilung grammatikalischer Fehler pro Modell", fontweight='bold')
rotate_labels(ax)
plt.savefig("grammar_errors.png", dpi=300, bbox_inches="tight")

# 3. Lesbarkeit
plt.figure(figsize=(12, 6))
ax = sns.pointplot(x="Model", y="Readability Score", data=df, capsize=0.1, palette="coolwarm")
plt.title("Durchschnittliche Lesbarkeit (Flesch Score)", fontweight='bold')
rotate_labels(ax)
plt.savefig("readability.png", dpi=300, bbox_inches="tight")

# 4. Sentiment-Analyse
sentiment_counts = df.groupby(["Model", "Sentiment"]).size().unstack().fillna(0)
sentiment_percent = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100

plt.figure(figsize=(14, 7))
ax = sentiment_percent.plot(kind="bar", stacked=True, colormap="RdYlGn")
plt.title("Sentiment-Verteilung der Antworten", fontweight='bold')
plt.ylabel("Anteil (%)")
plt.legend(title="Sentiment", bbox_to_anchor=(1.05, 1))
rotate_labels(ax)
plt.savefig("sentiment.png", dpi=300, bbox_inches="tight")

# 5. Kombiniertes Diagramm
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Subplot 1: BLEU & ROUGE
sns.barplot(ax=axes[0, 0], x="Model", y="Score", hue="Metric", data=df_melt)
axes[0, 0].set_title("Textqualität (BLEU & ROUGE)", fontweight='bold')
rotate_labels(axes[0, 0])

# Subplot 2: Grammatikfehler
sns.boxplot(ax=axes[0, 1], x="Model", y="Grammar Errors", data=df)
axes[0, 1].set_title("Grammatikalische Fehler", fontweight='bold')
rotate_labels(axes[0, 1])

# Subplot 3: Lesbarkeit
sns.pointplot(ax=axes[1, 0], x="Model", y="Readability Score", data=df)
axes[1, 0].set_title("Lesbarkeit", fontweight='bold')
rotate_labels(axes[1, 0])

# Subplot 4: Sentiment
sentiment_percent.plot(ax=axes[1, 1], kind="bar", stacked=True)
axes[1, 1].set_title("Sentiment", fontweight='bold')
rotate_labels(axes[1, 1])

plt.subplots_adjust(hspace=0.3, wspace=0.25)
plt.savefig("combined_metrics.png", dpi=300, bbox_inches="tight")

# Deskriptive Statistik
summary = df.groupby("Model")[["BLEU", "ROUGE-L", "Grammar Errors"]].agg(["mean", "std", "median", "min", "max"])
summary.to_latex("summary.tex", float_format="%.3f")