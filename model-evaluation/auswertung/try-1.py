import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np

# Set scientific style
# Updated style configuration section
plt.style.use('default')  # Reset to default first
sns.set_theme(style="whitegrid")  # Modern Seaborn theming
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'figure.figsize': (10, 6),
    'grid.color': '#e0e0e0',  # Add subtle grid
    'text.usetex': False       # Disable LaTeX if not installed
})

# Load and process data
def load_data():
    files = glob.glob("*.json")
    dfs = []
    
    for file in files:
        model_name = file.split("_")[-1].replace(".json", "")
        df = pd.read_json(file)
        df["Model"] = model_name
        dfs.append(df)
    
    combined_df = pd.concat(dfs)
    
    # Convert numeric columns
    numeric_cols = ["Response Time (seconds)", "CPU Usage (%)", "Memory Usage (MB)"]
    combined_df[numeric_cols] = combined_df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    
    return combined_df

# Figure 1: Response Time Comparison
def plot_response_times(df):
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x="Model", y="Response Time (seconds)", data=df,
                    showmeans=True, meanprops={"marker":"o", "markerfacecolor":"white"})
    
    # Add annotations
    medians = df.groupby("Model")["Response Time (seconds)"].median().values
    vertical_offset = df["Response Time (seconds)"].max() * 0.02
    
    for xtick in ax.get_xticks():
        ax.text(xtick, medians[xtick] + vertical_offset, f"{medians[xtick]:.2f}", 
                horizontalalignment='center', size=10, color='black')
    
    plt.title("Model Response Time Comparison", pad=20)
    plt.xlabel("AI Model")
    plt.ylabel("Response Time (s)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("response_time_comparison.pdf", bbox_inches='tight')
    plt.close()

# Figure 2: Resource Usage Comparison
def plot_resource_usage(df):
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # CPU Usage
    sns.lineplot(data=df, x="Prompt", y="CPU Usage (%)", hue="Model", 
                style="Model", markers=True, dashes=False, ax=ax1, 
                legend="brief", markersize=8)
    
    ax1.set_ylabel("CPU Utilization (%)", labelpad=15)
    ax1.set_xlabel("Prompt", labelpad=15)
    ax1.tick_params(axis='x', rotation=90)
    
    # Memory Usage
    ax2 = ax1.twinx()
    sns.lineplot(data=df, x="Prompt", y="Memory Usage (MB)", hue="Model",
                style="Model", markers=True, dashes=False, ax=ax2,
                legend=False, markersize=8, alpha=0.7)
    
    ax2.set_ylabel("Memory Consumption (MB)", labelpad=15)
    
    # Combine legends
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles=handles, labels=labels, loc='upper left', 
              bbox_to_anchor=(1.1, 1), frameon=True)
    
    plt.title("Computational Resource Utilization by Prompt and Model", pad=25)
    plt.tight_layout()
    plt.savefig("resource_utilization_comparison.pdf", bbox_inches='tight')
    plt.close()

# Generate summary table
def generate_summary_table(df):
    summary = df.groupby("Model").agg({
        "Response Time (seconds)": ["mean", "std"],
        "CPU Usage (%)": ["mean", "max"],
        "Memory Usage (MB)": ["mean", "max"]
    }).round(2)
    
    print("\nPerformance Summary Table:")
    print(summary.to_string())
    
    # Save to LaTeX
    with open("performance_summary.tex", "w") as f:
        f.write(summary.style.to_latex())

# Main execution
if __name__ == "__main__":
    df = load_data()
    plot_response_times(df)
    plot_resource_usage(df)
    generate_summary_table(df)