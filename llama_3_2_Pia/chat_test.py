import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the Llama model and tokenizer
model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Add a padding token (if missing)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding token

model = AutoModelForCausalLM.from_pretrained(model_name)

# Set the device to GPU or CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Chat loop
def chat():
    print("Llama Chat. Type 'exit' to stop the chat.")
    chat_history = ""

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Ending chat...")
            break

        # Append user input to chat history
        chat_history += f"User: {user_input}\n"

        # Tokenize and include the attention mask
        inputs = tokenizer(chat_history, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs.input_ids.to(device)
        attention_mask = inputs.attention_mask.to(device)

        # Generate response from the model with the attention mask
        with torch.no_grad():
            output = model.generate(input_ids, attention_mask=attention_mask, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)

        # Decode and clean up the response
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        response = response[len(chat_history):].strip()

        # Display the model's response
        print(f"Llama: {response}\n")

        # Append the model's response to the chat history
        chat_history += f"Llama: {response}\n"

# Start the chat
if __name__ == "__main__":
    chat()
