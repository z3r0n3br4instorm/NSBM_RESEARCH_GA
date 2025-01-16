from ollama import chat

class ModelComm:
    def __init__(self):
        self.model = "llama3.2"
        self.sessionContext = ""
        self.clearSessionContext = False

    def runChat(self, messageInput):
        self.speak = False
        self.stream = chat(
            self.model,
            messages=[
                {
                    "system": "You are a helpful assistant",
                    "role": "user",
                    "content": messageInput,
                }
            ],
            stream=True,
        )
        for chunk in self.stream:
            print(chunk["message"]["content"], end="", flush=True)
        self.speak = True
        return chunk["message"]["content"]

    # TODO: Context Memorization and Management
