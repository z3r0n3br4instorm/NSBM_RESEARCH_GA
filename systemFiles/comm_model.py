from ollama import chat

class ModelComm:
    def __init__(self):
        self.model = "llama3.2"
        self.session_context = []
        self.speak = False

    def add_to_context(self, role, content):
        self.session_context.append({"role": role, "content": content})

    def clear_context(self):
        self.session_context = []

    def run_chat(self, message_input):
        if self.execute_command(message_input):
            return self.execute_command(message_input)
        self.add_to_context("user", message_input)
        messages = [{"role": "system", "content": "You are a helpful assistant"}] + self.session_context
        self.speak = False
        stream = chat(self.model, messages=messages, stream=True)
        response_content = ""
        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)
            response_content += chunk["message"]["content"]
        self.speak = True
        self.add_to_context("assistant", response_content)
        return response_content

    def execute_command(self, command):
        if command.lower() == "clear":
            self.clear_context()
            print("Session context cleared.")
            return "Session context cleared."