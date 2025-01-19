from langchain_core.messages.base import message_to_dict
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms.ollama import Ollama
from queue import Queue
from threading import Thread
from datetime import datetime
from typing_extensions import Set

class log:
    def info(self, message):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOGGER][TD:{current_time}] {message}")

class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.queue.put(token)

    def on_llm_end(self, *args, **kwargs) -> None:
        self.queue.put(None)

class ModelComm:
    def __init__(self):
        self.token_queue = Queue()
        handler = StreamingHandler(self.token_queue)
        try:
            self.model = Ollama(model="lama3.2", callbacks=[handler])
        except:
            self.log.info("Error: Could not initialize Ollama model.")
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
        # self.execute_command(message_input)
        if message_input.lower() == "clear":
            self.clear_context()
            print("Session context cleared.")
            return "clr_cntxt"
        self.add_to_context("user", message_input)

        template = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.session_context])
        self.prompt = ChatPromptTemplate.from_template(template)

        try:
            self.chain = self.prompt | self.model
        except:
            self.log.info("Error: Could not initialize chain.")
            return "chain_error"

        stream_thread = Thread(target=self.process_tokens, args=(self.token_queue,))
        stream_thread.start()

        stream = self.chain.invoke({"question": message_input})
        response_content = ""

        self.add_to_context("assistant", response_content)

        # Wait for the streaming thread to finish
        stream_thread.join()

        return response_content
