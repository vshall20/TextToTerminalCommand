#!/usr/bin/env python3
import argparse
import os
import requests
import openai
import json
import re

# Initialize the OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
ollama_endpoint = 'http://localhost:11434/api/generate'  # Adjust this to your Ollama API endpoint

def extract_command(response_text):
    # Extract text within triple backticks
    print(response_text)
    commands = re.findall(r"```bash\s*\n(.*?)\n```", response_text, re.DOTALL)
    return commands
    # match = re.search(r"```bash\n(.+?)\n```", response_text, re.DOTALL)
    # print(match)
    # if match:
    #     return match.group(1).strip()
    # return "Command not found."
def convert_text_to_command_with_openai(text):
    prompt_text = f"Directly output a single command to run in terminal based on the Operating System mentioned to {text}.\n Do not give explanation, just output the command. If Operating System in not mentioned, assume it to be UNIX"
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=50
    )
    command = response.choices[0].message.content.strip()
    return command

def convert_text_to_command_with_ollama(text):
    """
    Use local Ollama API to convert text to a terminal command.
    """
    try:
        url = ollama_endpoint
        headers = {'Content-Type': 'application/json'}
        prompt_text = f"Provide a concise and single command based on the Operating System specified to {text}.\n Do not give explanation, just output the command"
        data = {
            "model": "deepseek-coder",
            "prompt": prompt_text,
            "stream": False
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(response)
        if response.status_code == 200:
            response_data = response.json()
            # commands = extract_command(response_data['response'])
            commands = response_data['response']
            return commands
        else:
            print(f"Failed to connect to Ollama API: {response.status_code}, {response.text}")
            raise Exception("Failed to connect to Ollama API")
    except Exception as e:
        print(f"Failed to connect to Ollama API: {response.status_code}, {response.text}")
        raise Exception("Failed to connect to Ollama API")


def main():
    parser = argparse.ArgumentParser(description='Convert text to terminal commands using AI.')
    parser.add_argument('text', nargs='?', help='Text to convert to command')
    parser.add_argument('--model', default='openai', help='AI model to use (openai or ollama)')
    args = parser.parse_args()


    if not args.text:
        print("No command text provided.")
        return

    if args.model.lower() == 'ollama':
        command = convert_text_to_command_with_ollama(args.text)
    else:
        command = convert_text_to_command_with_openai(args.text)

    print(f"Suggested Command: {command}")
    confirmation = input("Do you want to execute this command? (yes/no/edit) ")
    if confirmation.lower() == 'yes':
        os.system(command)
    elif confirmation.lower() == 'edit':
        custom_command = input("Enter your command: ")
        os.system(custom_command)

if __name__ == "__main__":
    main()