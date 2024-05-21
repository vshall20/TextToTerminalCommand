import os
import requests
import openai

# Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

ollama_endpoint = 'http://localhost:11434/api/generate'  # Adjust this to your Ollama API endpoint

def convert_text_to_command_with_openai(text):
    """
    Use OpenAI API to convert text to a terminal command.
    """
    try:
        prompt_text = f"Directly output a UNIX command to {text}."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Updated to use chat completions endpoint
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=50
        )
        print(f"Response object: {response}")
        command = response.choices[0].message.content.strip()
        return command
    except Exception as e:
        print(f"Error: {e}")
        print(f"Failed to convert text to command using OpenAI: {e}")
        return None

def convert_text_to_command_with_ollama(text):
    """
    Use local Ollama API to convert text to a terminal command.
    """
    try:
        url = ollama_endpoint
        headers = {'Content-Type': 'application/json'}
        prompt_text = f"Directly output a UNIX command to {text}."
        data = {
            "model": "deepseek-coder",
            "prompt": prompt_text,
            "stream": False
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response)
        if response.status_code == 200:
            command = response.json().get('command', '').strip()
            return command
        else:
            print(f"Failed to connect to Ollama API: {response.status_code}, {response.text}")
            raise Exception("Failed to connect to Ollama API")
    except Exception as e:
        print(f"Failed to connect to Ollama API: {response.status_code}, {response.text}")
        raise Exception("Failed to connect to Ollama API")

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