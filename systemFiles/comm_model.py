from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.base import BaseCallbackHandler
from langchain_community.llms.ollama import Ollama
from queue import Queue
from threading import Thread
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class Log:
    def info(self, message: str) -> None:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[LOGGER][{current_time}] {message}")


class ModelComm:
    def __init__(self):
        self.token_queue = Queue()
        self.log = Log()

        # Initialize the model
        try:
            self.model = Ollama(model="llama3.2")
        except Exception as e:
            self.log.info(f"Error initializing Ollama model: {e}")

        # Initialize memory and workflow
        self.memory = MemorySaver()
        self.setup_workflow()

    def setup_workflow(self):
        """LangGraph workflow for memory management."""
        self.workflow = StateGraph(state_schema=MessagesState)

        def call_model(state: MessagesState):
            system_prompt = "You are a helpful assistant. Answer all questions to the best of your ability."
            messages = [SystemMessage(content=system_prompt)] + state["messages"]
            response = self.model.invoke(messages)
            return {"messages": response}

        # Define workflow graph
        self.workflow.add_node("model", call_model)
        self.workflow.add_edge(START, "model")
        self.app = self.workflow.compile(checkpointer=self.memory)

    def reset_memory(self):
        """Memory Reset Logic"""
        self.memory = MemorySaver()  # Create a new MemorySaver instance
        self.setup_workflow()
        print("Session memory reset.")

    # def process_tokens(self, queue: Queue) -> None:
    #     """Processes tokens from the queue in real-time."""
    #     print("Streaming tokens:")
    #     while True:
    #         token = queue.get()
    #         if token is None:
    #             break
    #         print(token, end="", flush=True)
    #     print("\nStreaming complete.")

    def run_chat(self, message_input: str):
        if message_input.lower() == "clear":
            self.reset_memory()  # Reset memory by reinitializing
            return "clr_cntxt"

        user_message = HumanMessage(content=message_input)
        try:
            response = self.app.invoke(
                {"messages": [user_message]},
                config={"configurable": {"thread_id": "1"}},
            )
        except Exception as e:
            self.log.info(f"Error processing message: {e}")
            return "error"

        # Process and print the response from the assistant
        # stream_thread = Thread(target=self.process_tokens, args=(self.token_queue,))
        # stream_thread.start()

        assistant_response = response["messages"][-1]
        print(f"Assistant: {assistant_response.content}")
        # stream_thread.join()

        return assistant_response.content
