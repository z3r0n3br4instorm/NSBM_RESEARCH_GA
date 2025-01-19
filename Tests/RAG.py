import requests

def send_request_to_ollama(model, prompt, session_id):
    """
    Send a request to the locally running Ollama server.

    :param model: The name of the model to use (e.g., "llama").
    :param prompt: The user prompt to send.
    :param session_id: A unique session ID to maintain context.
    :return: The response from the server as a string.
    """
    url = "http://localhost:11434/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt,
        "session_id": session_id
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes >= 400
        return response.json().get("response", "No response from server.")
    except requests.RequestException as e:
        return f"Error communicating with Ollama server: {e}"

def main():
    # Define your model name and session ID
    model = "llama"  # Replace with your model name
    session_id = "123456789"  # Unique session ID to maintain context

    print("Chat with the Ollama server! Type 'exit' to quit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() == "exit":
            print("Goodbye!")
            break

        # Send the prompt to the server
        response = send_request_to_ollama(model, prompt, session_id)
        print(f"Ollama: {response}")

if __name__ == "__main__":
    main()
