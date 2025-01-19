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


def process_tokens(queue: Queue) -> None:
    """Process tokens from the queue in real time."""
    print("Streaming tokens:")
    while True:
        token = queue.get()
        if token is None:
            break
        print(token, end="", flush=True)
    print("\nStreaming complete.")


def main() -> None:
    # Queue for inter-thread communication
    token_queue = Queue()

    # Initialize the callback handler and LLM
    handler = StreamingHandler(token_queue)
    llm = Ollama(model="tinyllama", callbacks=[handler])

    # Start the LLM processing in a separate thread
    llm_thread = Thread(target=llm, args=("Your prompt here",))
    llm_thread.start()

    # Process tokens in the main thread
    process_tokens(token_queue)

    # Wait for the LLM thread to finish
    llm_thread.join()


if __name__ == "__main__":
    main()
