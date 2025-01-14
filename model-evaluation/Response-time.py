import time
import json
from ollama import chat

# Prompts for testing
prompts = [
    "Explain the theory of relativity in simple terms.",
    "Create a short story about a knight.",
    "What are the advantages of open-source projects?",
    "Write a Python function that outputs prime numbers up to 100.",
    "What is the difference between machine learning and deep learning?",
    "What are the key principles of quantum mechanics?",
    "Explain how photosynthesis works in plants.",
    "Describe the process of natural selection in evolutionary biology.",
    "What is the significance of the Renaissance period in European history?",
    "What is the Pythagorean theorem, and how is it used?",
    "Summarize the plot of a Shakespearean play of your choice.",
    "What is the main cause of the First World War?",
    "Describe the structure of an atom and the role of electrons.",
    "Write a SQL query that finds all customers older than 25.",
    "Explain the importance of data privacy in the digital age.",
    "How do blockchain technologies work?",
    "What are the effects of climate change on global ecosystems?",
    "Create a fictional dialogue between a historian and a time traveler.",
    "What is the role of mitochondria in the cell?",
    "Describe how a neural network processes input data.",
    "What are the advantages and disadvantages of space exploration?",
    "Write a Python script that reads a file and counts the words.",
    "Explain the key differences between capitalism and socialism.",
    "What is the significance of Ada Lovelace in computer science?",
    "What are the psychological effects of prolonged isolation?",
    "How does the immune system respond to a viral infection?",
    "Write a persuasive argument for the use of renewable energy.",
    "Create a summary of the book '1984' by George Orwell.",
    "What are the common patterns in machine learning algorithms?",
    "Explain the difference between supervised and unsupervised learning.",
    "What is the Turing Test, and how does it measure artificial intelligence?",
    "Describe the cultural impact of the Renaissance on modern society.",
    "What are the principles of democratic governance?",
    "Explain the process of photosynthesis in detail.",
    "How does a search engine like Google index the web?",
    "What is the significance of the Higgs boson in physics?",
    "Describe the evolution of language in early human civilizations.",
    "How does encryption work in secure messaging apps?",
    "Write a story about an astronaut on Mars discovering life.",
    "What are the ethical concerns surrounding genetic modification?",
    "Explain how a car engine converts fuel into motion.",
    "What are the cultural differences between Eastern and Western philosophies?",
    "How does quantum computing differ from classical computing?",
    "What are the main components of a healthy diet?",
    "Explain the importance of biodiversity in ecosystems.",
    "Describe the history of the internet and its evolution.",
    "What are the different stages of project management?",
    "Write a Python function to scrape data from a web page.",
    "What are the long-term effects of plastic pollution in oceans?",
    "Explain how machine learning can be used in healthcare.",
    "What is the concept of time dilation in Einstein's theory?",
    "Describe how democracy differs from autocracy.",
    "What are the advantages of multilingualism in society?",
    "Explain the basics of game theory and provide an example.",
    "Describe the cultural and historical significance of the Great Wall of China.",
    "What is the role of literature in shaping societal values?",
    "How do satellites help in disaster management?",
    "Write a Python script that converts temperature from Celsius to Fahrenheit.",
    "What are the different forms of renewable energy?",
    "Explain the significance of the moon landing in 1969.",
    "What are the differences between Roman and Greek architecture?",
    "Describe the economic impact of pandemics throughout history.",
    "What is the importance of financial literacy in modern society?",
    "How does artificial intelligence impact job markets?",
    "Explain how photosynthesis differs between C3 and C4 plants.",
    "What are the basic principles of quantum entanglement?",
    "Write a Python function to generate Fibonacci numbers.",
    "Explain the process of human memory formation.",
    "What is the impact of social media on mental health?",
    "Describe the history and cultural significance of the Olympic Games.",
    "Generate a D&D character with a backstory and traits.",
]

# Model name
model_name = "qwen2.5-coder:0.5b"

# Store results
results = []

# Loop through prompts
for prompt in prompts:
    try:
        start_time = time.time()
        # Ollama chat request
        response = chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        end_time = time.time()

        latency = end_time - start_time

        # Handle response as a dictionary
        if isinstance(response, dict) and 'message' in response and 'content' in response['message']:
            response_text = response['message']['content']
        else:
            response_text = "No content returned or unexpected format"

        print(f"Prompt: {prompt}\nResponse Time: {latency:.2f} seconds\n")

        # Save the result
        results.append({"Prompt": prompt, "Response Time (seconds)": latency, "Response": response_text})
    except Exception as e:
        print(f"Error with prompt '{prompt}': {e}")
        results.append({"Prompt": prompt, "Response Time (seconds)": "Error", "Response": f"Error: {str(e)}"})

# Save to JSON file
json_file_name = "ollama_response_time_results.json"
with open(json_file_name, "w") as file:
    json.dump(results, file, indent=4)

print(f"The results have been saved in {json_file_name}.")
