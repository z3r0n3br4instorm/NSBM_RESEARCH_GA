# Prototype Program For GA Core
from weakref import proxy
from systemFiles.comm_model import ModelComm
from systemFiles.RAG_NEW import RAG_Engine
from systemFiles.RAG_NEW import WebRag_Engine
global version
version = "0.1.1[refined]"
updates = "langchain RAG"

# Example Usage
if __name__ == "__main__":
    rag = RAG_Engine("llama3.2")
    # gamodel = ModelComm()
    print(f"- Debug Interface {version}-")
    print(f"Updates: {updates}")
    while True:
        print("\n")
        prompt = input(">")
        print("System is processing your request...")
        web_rag = WebRag_Engine().retrieveData(prompt)
        print(rag.processText("\n".join(web_rag), prompt)["answer"])
