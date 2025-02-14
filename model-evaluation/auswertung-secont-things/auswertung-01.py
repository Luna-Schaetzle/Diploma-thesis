import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =============================================================================
# Data Aggregation and Visualization for Model Performance Metrics
# =============================================================================
# This script aggregates experimental results from JSON files, each containing 
# performance metrics (e.g., BLEU, ROUGE, grammatical errors, readability, sentiment)
# for various AI models. The data are visualized using high-quality plots for scientific 
# analysis, and descriptive statistics are exported in LaTeX format.

# -----------------------------
# Data Aggregation
# -----------------------------
directory = "./"
aggregated_data = []
for file in os.listdir(directory):
    # Process files that follow the naming convention "scored_<model>.json"
    if file.startswith("scored_") and file.endswith(".json"):
        model = file.replace("scored_", "").replace(".json", "")
        df_temp = pd.read_json(os.path.join(directory, file))
        df_temp["Model"] = model
        aggregated_data.append(df_temp)
df = pd.concat(aggregated_data, ignore_index=True)

# -----------------------------
# Global Plotting Style Settings
# -----------------------------
sns.set_theme(style="whitegrid", font_scale=0.9)
plt.rcParams['axes.titlepad'] = 15
plt.rcParams['axes.labelpad'] = 10

def rotate_labels(ax, rotation: int = 45, ha: str = 'right') -> None:
    """
    Rotate the x-axis labels for improved readability.

    Parameters:
        ax (matplotlib.axes.Axes): The axes on which to rotate the labels.
        rotation (int): Angle in degrees to rotate the labels.
        ha (str): Horizontal alignment of the labels.
    """
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation, ha=ha, fontsize=9)
    plt.tight_layout()

# =============================================================================
# Visualization of Performance Metrics
# =============================================================================

# --- 1. BLEU and ROUGE Scores ---
plt.figure(figsize=(14, 7))
# Reshape data for plotting multiple text quality metrics
df_melt = df.melt(id_vars=["Model"], value_vars=["BLEU", "ROUGE-1", "ROUGE-2", "ROUGE-L"], 
                  var_name="Metric", value_name="Score")
ax = sns.barplot(x="Model", y="Score", hue="Metric", data=df_melt, palette="viridis")
plt.title("Comparison of BLEU and ROUGE Scores", fontweight='bold')
plt.ylim(0, 0.05)
plt.legend(loc="upper right", frameon=True)
rotate_labels(ax)
plt.savefig("bleu_rouge.png", dpi=300, bbox_inches="tight")

# --- 2. Grammatical Errors ---
plt.figure(figsize=(12, 6))
ax = sns.boxplot(x="Model", y="Grammar Errors", data=df, palette="Set2")
plt.title("Distribution of Grammatical Errors per Model", fontweight='bold')
rotate_labels(ax)
plt.savefig("grammar_errors.png", dpi=300, bbox_inches="tight")

# --- 3. Readability (Flesch Score) ---
plt.figure(figsize=(12, 6))
ax = sns.pointplot(x="Model", y="Readability Score", data=df, capsize=0.1, palette="coolwarm")
plt.title("Average Readability (Flesch Score)", fontweight='bold')
rotate_labels(ax)
plt.savefig("readability.png", dpi=300, bbox_inches="tight")

# --- 4. Sentiment Analysis ---
# Compute relative frequency of sentiment labels per model
sentiment_counts = df.groupby(["Model", "Sentiment"]).size().unstack().fillna(0)
sentiment_percent = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0) * 100

plt.figure(figsize=(14, 7))
ax = sentiment_percent.plot(kind="bar", stacked=True, colormap="RdYlGn")
plt.title("Sentiment Distribution of Responses", fontweight='bold')
plt.ylabel("Percentage (%)")
plt.legend(title="Sentiment", bbox_to_anchor=(1.05, 1))
rotate_labels(ax)
plt.savefig("sentiment.png", dpi=300, bbox_inches="tight")

# --- 5. Combined Metrics Overview ---
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Subplot 1: BLEU & ROUGE Metrics
sns.barplot(ax=axes[0, 0], x="Model", y="Score", hue="Metric", data=df_melt)
axes[0, 0].set_title("Text Quality (BLEU & ROUGE)", fontweight='bold')
rotate_labels(axes[0, 0])

# Subplot 2: Grammatical Errors
sns.boxplot(ax=axes[0, 1], x="Model", y="Grammar Errors", data=df, palette="Set2")
axes[0, 1].set_title("Grammatical Errors", fontweight='bold')
rotate_labels(axes[0, 1])

# Subplot 3: Readability
sns.pointplot(ax=axes[1, 0], x="Model", y="Readability Score", data=df, capsize=0.1, palette="coolwarm")
axes[1, 0].set_title("Readability", fontweight='bold')
rotate_labels(axes[1, 0])

# Subplot 4: Sentiment
sentiment_percent.plot(ax=axes[1, 1], kind="bar", stacked=True, colormap="RdYlGn")
axes[1, 1].set_title("Sentiment", fontweight='bold')
rotate_labels(axes[1, 1])

plt.subplots_adjust(hspace=0.3, wspace=0.25)
plt.savefig("combined_metrics.png", dpi=300, bbox_inches="tight")

# =============================================================================
# Descriptive Statistics Export
# =============================================================================
# Compute summary statistics for selected metrics by model
summary = df.groupby("Model")[["BLEU", "ROUGE-L", "Grammar Errors"]].agg(["mean", "std", "median", "min", "max"])
summary.to_latex("summary.tex", float_format="%.3f")
