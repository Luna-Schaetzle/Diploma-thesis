import json
import pandas as pd
import matplotlib.pyplot as plt

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def create_dataframe(data):
    """Convert JSON data to a pandas DataFrame and preprocess it."""
    df = pd.DataFrame(data)

    # Filter out rows with 'Error' in numerical columns
    numeric_columns = ["Response Time (seconds)", "CPU Usage (%)", "Memory Usage (MB)"]
    df = df[~df[numeric_columns].applymap(lambda x: isinstance(x, str)).any(axis=1)]

    # Convert columns to numeric
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    return df

def plot_response_time(df):
    """Create a bar plot for response time comparison."""
    plt.figure(figsize=(10, 6))
    df.plot(x="Prompt", y="Response Time (seconds)", kind="bar", legend=False, color="skyblue")
    plt.title("Response Time Comparison")
    plt.ylabel("Time (seconds)")
    plt.xlabel("Prompts")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def plot_cpu_memory_usage(df):
    """Create a bar plot for CPU and Memory usage comparison."""
    plt.figure(figsize=(10, 6))
    df.plot(x="Prompt", y=["CPU Usage (%)", "Memory Usage (MB)"], kind="bar", width=0.8)
    plt.title("CPU and Memory Usage Comparison")
    plt.ylabel("Usage")
    plt.xlabel("Prompts")
    plt.xticks(rotation=45, ha="right")
    plt.legend(["CPU Usage (%)", "Memory Usage (MB)"])
    plt.tight_layout()
    plt.show()

def main():
    file_path = input("Enter the path to the JSON file: ")

    try:
        # Load and preprocess data
        data = load_json(file_path)
        df = create_dataframe(data)

        # Generate plots
        plot_response_time(df)
        plot_cpu_memory_usage(df)
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
