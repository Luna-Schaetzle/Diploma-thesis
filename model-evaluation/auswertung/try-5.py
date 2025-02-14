import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np
import os
import logging

# Set up logging for consistent error and information messages.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Set scientific plotting style with an increased default figure height.
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
    'figure.figsize': (8, 10),  # Erhöhter Standardwert: Breite 8, Höhe 10
    'grid.color': '#e0e0e0',
    'axes.spines.right': False,
    'axes.spines.top': False
})

def load_and_process_data() -> pd.DataFrame:
    """
    Loads and processes all JSON files in the current directory.
    
    This function searches for all files matching "*.json", reads them into pandas DataFrames,
    assigns a 'Model' column based on the file name (without extension), converts specified
    numeric columns to numeric type, and removes rows with missing values in those columns.
    
    Returns:
        pd.DataFrame: A concatenated and cleaned DataFrame containing all data.
    """
    json_files = glob.glob("*.json")
    if not json_files:
        logging.warning("No JSON files found in the current directory.")
        return pd.DataFrame()
    
    dfs = []
    for file in json_files:
        try:
            model_name = os.path.splitext(file)[0]
            df = pd.read_json(file)
            df['Model'] = model_name
            dfs.append(df)
        except Exception as e:
            logging.error(f"Error loading {file}: {e}")
    
    if not dfs:
        logging.error("No data could be loaded from the JSON files.")
        return pd.DataFrame()
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Convert selected columns to numeric and drop rows with missing values in these columns.
    numeric_cols = ['Response Time (seconds)', 'CPU Usage (%)', 'Memory Usage (MB)']
    combined_df[numeric_cols] = combined_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    combined_df = combined_df.dropna(subset=numeric_cols)
    
    return combined_df

def create_resource_plot(df: pd.DataFrame, metric: str, title: str, ylabel: str, filename: str) -> None:
    """
    Creates a resource usage plot with violin and strip plots, annotated with statistical measures.
    
    The function generates a violin plot for the given metric across different AI models, overlays a strip plot
    to display individual data points, and annotates each model with its median and mean absolute deviation (MAD).
    The resulting plot is saved in both PDF and PNG formats.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the metric and 'Model' columns.
        metric (str): The column name representing the metric to be visualized.
        title (str): The title of the plot.
        ylabel (str): The label for the y-axis.
        filename (str): Base filename used for saving the plot.
    """
    # Noch höhere Grafik: figsize von (10,10)
    plt.figure(figsize=(10, 10))
    
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
    
    # Calculate median and mean absolute deviation (MAD) for each model.
    stats = df.groupby('Model')[metric].agg(median='median', mad=lambda x: np.mean(np.abs(x - x.median())))
    
    # Annotate each model with the calculated median and MAD.
    for xtick, model in enumerate(stats.index):
        model_stats = stats.loc[model]
        annotation = f"Med: {model_stats['median']:.1f}\nMAD: {model_stats['mad']:.1f}"
        # Position annotation at 5% above the minimum value.
        y_pos = df[metric].min() + (df[metric].max() - df[metric].min()) * 0.05
        ax.text(
            xtick,
            y_pos,
            annotation,
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
    
    # Save the plot in both vector (PDF) and raster (PNG) formats.
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')
    plt.savefig(f'{filename}.png', bbox_inches='tight')
    plt.close()

def plot_cpu_memory_comparison(df: pd.DataFrame) -> None:
    """
    Generates comparative plots for CPU usage and memory consumption across AI models.
    
    This function calls 'create_resource_plot' for both CPU and Memory metrics.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing performance metrics.
    """
    create_resource_plot(
        df=df,
        metric='CPU Usage (%)',
        title='Comparative Analysis of CPU Utilization Across AI Models',
        ylabel='CPU Usage (%)',
        filename='model_cpu_usage_comparison'
    )
    
    create_resource_plot(
        df=df,
        metric='Memory Usage (MB)',
        title='Comparative Analysis of Memory Consumption Across AI Models',
        ylabel='Memory Usage (MB)',
        filename='model_memory_usage_comparison'
    )

def generate_advanced_statistics(df: pd.DataFrame) -> None:
    """
    Generates advanced performance statistics for AI models and outputs the results both in the console and as a LaTeX table.
    
    The statistics include mean, standard deviation, and maximum values for CPU and memory usage,
    as well as mean and standard deviation for response times.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing performance metrics.
    """
    stats = df.groupby('Model').agg({
        'CPU Usage (%)': ['mean', 'std', 'max'],
        'Memory Usage (MB)': ['mean', 'std', 'max'],
        'Response Time (seconds)': ['mean', 'std']
    })
    
    print("\nAdvanced Performance Statistics:")
    print(stats.round(2).to_string())
    
    # Export the statistics as a formatted LaTeX table.
    try:
        latex_str = stats.style.format({
            ('CPU Usage (%)', 'mean'): "{:.1f}",
            ('Memory Usage (MB)', 'mean'): "{:.1f}"
        }).to_latex(
            hrules=True,
            caption="Model Performance Statistics",
            label="tab:model_stats"
        )
        with open('resource_stats.tex', 'w') as f:
            f.write(latex_str)
    except Exception as e:
        logging.error(f"Error generating LaTeX table: {e}")

def plot_response_times(df: pd.DataFrame) -> None:
    """
    Creates a comparative boxplot for model response times overlaid with a swarm plot for individual data points.
    
    The function annotates each AI model with its median response time and saves the plot in both PDF and PNG formats.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the 'Response Time (seconds)' and 'Model' columns.
    """
    # Noch höhere Grafik: figsize von (8,10)
    plt.figure(figsize=(8, 10))
    
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
    
    # Annotate the median response time for each model.
    medians = df.groupby('Model')['Response Time (seconds)'].median()
    for xtick, model in enumerate(medians.index):
        median_val = medians.loc[model]
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
    
    plt.savefig('model_response_times_comparison.pdf', bbox_inches='tight')
    plt.savefig('model_response_times_comparison.png', bbox_inches='tight')
    plt.close()

def generate_statistics(df: pd.DataFrame) -> None:
    """
    Generates a statistical summary of response times for each AI model and exports the results.
    
    The summary includes the mean, standard deviation, minimum, median, and maximum values.
    The results are printed to the console and saved as a LaTeX table.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the 'Response Time (seconds)' and 'Model' columns.
    """
    stats = df.groupby('Model')['Response Time (seconds)'].describe()
    print("\nResponse Time Statistics:")
    print(stats[['mean', 'std', 'min', '50%', 'max']].round(3).to_string())
    
    try:
        with open('response_stats.tex', 'w') as f:
            f.write(
                stats[['mean', 'std', 'min', '50%', 'max']]
                .round(3)
                .style.to_latex(hrules=True)
            )
    except Exception as e:
        logging.error(f"Error generating LaTeX response stats: {e}")

def main() -> None:
    """
    Main execution function.
    
    Loads and processes data from JSON files, generates various comparative plots (response times, CPU, and memory usage),
    and outputs advanced performance statistics along with their LaTeX representations.
    """
    df = load_and_process_data()
    if df.empty:
        logging.error("No data available for plotting and analysis.")
        return
    
    plot_response_times(df)
    plot_cpu_memory_comparison(df)
    generate_advanced_statistics(df)
    generate_statistics(df)

if __name__ == "__main__":
    main()
