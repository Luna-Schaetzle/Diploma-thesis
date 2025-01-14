import time
import json
import psutil  # For CPU, memory usage
from ollama import chat

# Prompts for testing
prompts = [
    "Explain the theory of relativity in simple terms.",
    "Create a short story about a knight.",
    "What are the advantages of open-source projects?",
    "Write a Python function that outputs prime numbers up to 100.",
    "What is the difference between machine learning and deep learning?",
    "What are the basic principles of quantum entanglement?",
    "Write a Python function to generate Fibonacci numbers.",
    "Explain the process of human memory formation.",
    "What is the impact of social media on mental health?",
    "Describe the history and cultural significance of the Olympic Games.",
    "Generate a D&D character with a backstory and traits."
]

# Model name
model_name = "qwen2.5-coder:0.5b"

# Store results
results = []

# Function to get GPU usage if available
def get_gpu_usage():
    try:
        import torch
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.memory_allocated() / (1024 ** 2)  # Convert to MB
            gpu_utilization = torch.cuda.utilization(0) if hasattr(torch.cuda, 'utilization') else "N/A"
            return gpu_memory, gpu_utilization
        else:
            return 0, "No GPU detected"
    except ImportError:
        return 0, "torch not installed"

# Loop through prompts
for prompt in prompts:
    try:
        # Measure system usage before model execution
        cpu_before = psutil.cpu_percent(interval=None)
        memory_before = psutil.virtual_memory().used / (1024 ** 2)  # Convert to MB

        start_time = time.time()
        # Ollama chat request
        response = chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        end_time = time.time()

        latency = end_time - start_time

        # Measure system usage after model execution
        cpu_after = psutil.cpu_percent(interval=None)
        memory_after = psutil.virtual_memory().used / (1024 ** 2)  # Convert to MB

        cpu_usage = cpu_after - cpu_before
        memory_usage = memory_after - memory_before
        gpu_memory_usage, gpu_utilization = get_gpu_usage()

        # Extract content from the Message object
        if response and hasattr(response["message"], "content"):
            response_text = response["message"].content  # Accessing the attribute of the Message object
        else:
            response_text = "No content returned or unexpected format"

        print(f"Prompt: {prompt}\nResponse Time: {latency:.2f} seconds\n")

        # Save the result
        results.append({
            "Prompt": prompt,
            "Response Time (seconds)": latency,
            "Response": response_text,
            "CPU Usage (%)": cpu_usage,
            "Memory Usage (MB)": memory_usage,
            "GPU Memory Usage (MB)": gpu_memory_usage,
            "GPU Utilization (%)": gpu_utilization
        })
    except Exception as e:
        print(f"Error with prompt '{prompt}': {e}")
        results.append({
            "Prompt": prompt,
            "Response Time (seconds)": "Error",
            "Response": f"Error: {str(e)}",
            "CPU Usage (%)": "N/A",
            "Memory Usage (MB)": "N/A",
            "GPU Memory Usage (MB)": "N/A",
            "GPU Utilization (%)": "N/A"
        })

# Save to JSON file
json_file_name = model_name + "_response_time_results_ressours_usage.json"
with open(json_file_name, "w") as file:
    json.dump(results, file, indent=4)

print(f"The results have been saved in {json_file_name}.")
