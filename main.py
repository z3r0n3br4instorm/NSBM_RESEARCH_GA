# Prototype Program For GA Core
from systemFiles.comm_model import ModelComm
from systemFiles.RAG import RAG_Engine
global version
version = "0.0.2"

# Example Usage
if __name__ == "__main__":
    topics = [
        "distributed systems",
        "networking",
        "cloud computing",
        "databases",
        "nsbm",
    ]
    rag = RAG_Engine(topics)
    gamodel = ModelComm()
    print(f"- Demo Interface {version}-")
    while True:
        prompt = input(">")
        rag.runPrompt(prompt)
        ragContext = rag.ragResearchOn("systemFiles/GADB.db")
        if ragContext is not None:
            prompt = f"""$$DATA_FROM_RAG_ENGINE:\n{ragContext}
                        \nDATA_FROM_RAG_ENGINE_END$$\n{prompt}
                    """
        print(f"{gamodel.runChat(prompt)}")
