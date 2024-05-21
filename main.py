import os
import openai
import requests

# Set up API keys or endpoints using environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
ollama_endpoint = 'http://localhost:5000/convert'  # Assuming Ollama runs on localhost port 5000

def convert_text_to_command_with_openai(text):
    """
    Use OpenAI API to convert text to a terminal command.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can change the model as needed
            prompt=f"Convert the following user instruction into a safe terminal command:\n\n'{text}'",
            max_tokens=50
        )
        command = response.choices[0].text.strip()
        return command
    except Exception as e:
        print("Failed to convert text to command using OpenAI:", e)
        return None

def convert_text_to_command_with_ollama(text):
    """
    Use local Ollama API to convert text to a terminal command.
    """
    try:
        response = requests.post(ollama_endpoint, json={"text": text})
        if response.status_code == 200:
            command = response.json().get('command', '').strip()
            return command
        else:
            print("Ollama API error:", response.text)
            return None
    except Exception as e:
        print("Failed to convert text to command using Ollama:", e)
        return None

def main():
    # Let the user choose the AI provider
    ai_provider = input("Choose AI provider (OpenAI or Ollama): ").strip().lower()
    while True:
        user_input = input("heyGPT: ")
        if user_input.lower() == 'exit':
            break
        if ai_provider == 'openai':
            suggested_command = convert_text_to_command_with_openai(user_input)
        elif ai_provider == 'ollama':
            suggested_command = convert_text_to_command_with_ollama(user_input)
        else:
            print("Invalid AI provider. Please restart the program with the correct provider.")
            break

        if suggested_command:
            print("Suggested Command:", suggested_command)
            confirmation = input("Do you want to execute this command? (yes/no/edit) ")
            if confirmation.lower() == 'yes':
                print(f"Executing: {suggested_command}")
            elif confirmation.lower() == 'edit':
                custom_command = input("Enter your command: ")
                print(f"Executing: {custom_command}")
            else:
                print("Command execution canceled.")
        else:
            print("Could not generate a valid command. Please try again.")

if __name__ == "__main__":
    main()