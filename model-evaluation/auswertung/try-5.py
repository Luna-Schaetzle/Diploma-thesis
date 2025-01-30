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
            model_name = os.path.splitext(file)[0]
            df = pd.read_json(file)
            df['Model'] = model_name
            dfs.append(df)
        except Exception as e:
            print(f"Fehler beim Laden von {file}: {e}")
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Datenbereinigung für alle numerischen Spalten
    numeric_cols = ['Response Time (seconds)', 'CPU Usage (%)', 'Memory Usage (MB)']
    combined_df[numeric_cols] = combined_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    return combined_df.dropna(subset=numeric_cols)

def create_resource_plot(df, metric, title, ylabel, filename):
    """Erstellt ein Ressourcen-Nutzungs-Diagramm"""
    plt.figure(figsize=(10, 6))
    
    # Violinplot + Stripplot für detaillierte Verteilung
    ax = sns.violinplot(
        x='Model',
        y=metric,
        data=df,
        inner='quartile',
        palette='muted',
        cut=0
    )
    
    sns.stripplot(
        x='Model',
        y=metric,
        data=df,
        color='#303030',
        size=2.5,
        alpha=0.7
    )
    
    # Statistische Anmerkungen (Median + Mean Absolute Deviation)
    stats = df.groupby('Model')[metric].agg(['median', lambda x: np.mean(np.abs(x - x.median()))])
    stats.columns = ['median', 'mad']
    for xtick in ax.get_xticks():
        model_stats = stats.iloc[xtick]
        ax.text(
            xtick,
            df[metric].max() * 0.05,
            f"Med: {model_stats['median']:.1f}\nMAD: {model_stats['mad']:.1f}",
            ha='center',
            va='bottom',
            fontsize=8,
            color='#404040'
        )
    
    plt.title(title, pad=15)
    plt.xlabel('AI Model', labelpad=12)
    plt.ylabel(ylabel, labelpad=12)
    plt.xticks(rotation=45, ha='right')
    plt.ylim(bottom=0)
    plt.tight_layout()
    
    # Speichern in Vektor- und Rasterformaten
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')
    plt.savefig(f'{filename}.png', bbox_inches='tight')
    plt.close()

def plot_cpu_memory_comparison(df):
    """Erstellt kombinierte CPU/Memory-Diagramme"""
    # CPU Auslastung
    create_resource_plot(
        df=df,
        metric='CPU Usage (%)',
        title='Comparative Analysis of CPU Utilization Across AI Models',
        ylabel='CPU Usage (%)',
        filename='model_cpu_usage_comparison'
    )
    
    # Memory Auslastung
    create_resource_plot(
        df=df,
        metric='Memory Usage (MB)',
        title='Comparative Analysis of Memory Consumption Across AI Models',
        ylabel='Memory Usage (MB)',
        filename='model_memory_usage_comparison'
    )

def generate_advanced_statistics(df):
    """Generiert erweiterte Statistiken"""
    stats = df.groupby('Model').agg({
        'CPU Usage (%)': ['mean', 'std', 'max'],
        'Memory Usage (MB)': ['mean', 'std', 'max'],
        'Response Time (seconds)': ['mean', 'std']
    })
    
    # Formatierte Ausgabe
    print("\nAdvanced Performance Statistics:")
    print(stats.round(2).to_string())
    
    # LaTeX-Ausgabe
    with open('resource_stats.tex', 'w') as f:
        latex_str = stats.style.format(
            "{:.1f}", subset=[('CPU Usage (%)', 'mean'), ('Memory Usage (MB)', 'mean')]
        ).to_latex(
            hrules=True,
            caption="Model Performance Statistics",
            label="tab:model_stats"
        )
        f.write(latex_str)

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
        palette='muted'
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
    
    plt.title('Comparative Analysis of Model Response Times', pad=15)
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
    plot_response_times(df)  # Deine existierende Response-Time-Funktion
    plot_cpu_memory_comparison(df)
    generate_advanced_statistics(df)