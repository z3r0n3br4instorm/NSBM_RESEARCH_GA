from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms.ollama import Ollama
from queue import Queue
from threading import Thread

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)

    def on_llm_end(self, **kwargs) -> None:
        self.queue.put(None)

class ModelComm:
    def __init__(self):
        self.model = Ollama(model="llama3.2")
        self.session_context = []

    def add_to_context(self, role, content):
        self.session_context.append({"role": role, "content": content})

    def clear_context(self):
        self.session_context = []

    def process_tokens(self, queue: Queue) -> None:
        """Process tokens from the queue in real time."""
        print("Streaming tokens:")
        while True:
            token = queue.get()
            if token is None:
                break
            print(token, end="", flush=True)
        print("\nStreaming complete.")

    def run_chat(self, message_input):
        self.add_to_context("user", message_input)

        template = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.session_context])

        token_queue = Queue()
        handler = StreamingHandler(token_queue)
        self.model = Ollama(model="tinyllama", callbacks=[handler])
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = self.prompt | self.model

        stream_thread = Thread(target=self.process_tokens, args=(token_queue,))
        stream_thread.start()

        stream = self.chain.invoke({"question": message_input})
        response_content = ""

        self.add_to_context("assistant", response_content)

        # Wait for the streaming thread to finish
        stream_thread.join()

        return response_content

    def execute_command(self, command):
        if command.lower() == "clear":
            self.clear_context()
            print("Session context cleared.")
            return "Session context cleared."
