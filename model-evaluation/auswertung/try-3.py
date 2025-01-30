import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np
import os

# Wissenschaftliches Design
plt.style.use('default')
sns.set_theme(style="whitegrid", context="paper")
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'figure.figsize': (8, 5),
    'grid.color': '#e0e0e0',
    'axes.spines.right': False,
    'axes.spines.top': False
})

def load_and_process_data():
    """Lädt und verarbeitet alle JSON-Dateien im Verzeichnis"""
    files = glob.glob("*.json")
    
    dfs = []
    for file in files:
        try:
            model_name = os.path.splitext(file)[0].replace('_results', '')
            df = pd.read_json(file)
            df['Model'] = model_name
            dfs.append(df)
        except Exception as e:
            print(f"Fehler beim Laden von {file}: {e}")
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Datenbereinigung
    combined_df['Response Time (seconds)'] = pd.to_numeric(
        combined_df['Response Time (seconds)'], errors='coerce'
    )
    return combined_df.dropna(subset=['Response Time (seconds)'])

def plot_response_times(df):
    """Erstellt das Response Time Diagramm"""
    plt.figure(figsize=(8, 5))
    
    # Boxplot mit Swarmplot überlagert
    ax = sns.boxplot(
        x='Model',
        y='Response Time (seconds)',
        data=df,
        width=0.6,
        showfliers=False,
        palette='pastel'
    )
    
    sns.swarmplot(
        x='Model',
        y='Response Time (seconds)',
        data=df,
        color='#404040',
        size=3,
        alpha=0.6
    )
    
    # Medianwerte annotieren
    medians = df.groupby('Model')['Response Time (seconds)'].median()
    for xtick in ax.get_xticks():
        median_val = medians.iloc[xtick]
        ax.text(
            xtick,
            median_val + 0.05,
            f'{median_val:.2f}s',
            ha='center',
            va='bottom',
            fontsize=8,
            color='#2f2f2f'
        )
    
    plt.title('Model Response Time Comparison', pad=15)
    plt.xlabel('AI Model', labelpad=10)
    plt.ylabel('Response Time (seconds)', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Speichern in verschiedenen Formaten
    plt.savefig('model_response_times_comparison.pdf', bbox_inches='tight')
    plt.savefig('model_response_times_comparison.png', bbox_inches='tight')
    plt.close()

def generate_statistics(df):
    """Generiert statistische Zusammenfassung"""
    stats = df.groupby('Model')['Response Time (seconds)'].describe()
    print("\nResponse Time Statistics:")
    print(stats[['mean', 'std', 'min', '50%', 'max']].round(3).to_string())
    
    # Latex-Tabelle
    with open('response_stats.tex', 'w') as f:
        f.write(
            stats[['mean', 'std', 'min', '50%', 'max']]
            .round(3)
            .style.to_latex(hrules=True)
        )

if __name__ == "__main__":
    df = load_and_process_data()
    plot_response_times(df)
    generate_statistics(df)