# import spacy
# import sqlite3
# from langchain import text_splitter
import requests
from bs4 import BeautifulSoup
#---- Unstable Updates
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from googlesearch import search
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import random
#----

class RAG_Engine:
    def __init__(self, target):
        self.targetModelName = target
        self.targetLLM = Ollama(model=self.targetModelName, base_url="http://127.0.0.1:11434")
        self.embedder = OllamaEmbeddings(model = self.targetModelName, base_url='http://127.0.0.1:11434')
        # Generate a random sessionID using random library
        self.memory = ConversationBufferMemory(memory_key=f"{random.random()}", return_messages=True)

    def processText(self, data, prompt):
        text_splitter =  RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
        chunks = text_splitter.split_text(data)
        vector_store = Chroma.from_texts(chunks, self.embedder)
        retriever = vector_store.as_retriever()
        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
        combine_docs_chain = create_stuff_documents_chain(
            self.targetLLM, retrieval_qa_chat_prompt
        )
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
        response = retrieval_chain.invoke({"input": prompt, "chat_history": self.memory.chat_memory.messages})
        self.memory.save_context({"input": prompt}, {"output": response["answer"]})
        return response

class WebRag_Engine:
    def __init__(self):
        self.researchWebsites = [
            "https://www.wikipedia.org",
            "https://www.bbc.co.uk",
            "https://www.nsbm.ac.lk",
            "https://www.google.com",
            "https://www.youtube.com",
        ]

    def retrieveData(self, query, num_results=10):
        results = []
        try:
            for url in search(query, num=num_results, stop=num_results, pause=2):
                results.append(f"Found result: {url}")
        except Exception as e:
            results.append(f"Error performing Google search: {e}")

        return results if results else ["No results found."]

if __name__ == "__main__":
    # topics = ["Artificial Intelligence", "Machine Learning", "Natural Language Processing"]
    # query = "What is NSBM Green University?"

    web_rag = WebRag_Engine()
    while True:
        query = input(">")
        print("System is processing your request...")
        print(web_rag.retrieveData(query))
        print(web_rag)
        #
        # New Implementation
        rag = RAG_Engine("tinyllama")
        search_results = web_rag.retrieveData(query)  # Get search results
        search_results_text = "\n".join(search_results)  # Convert list to a single string
        print(rag.processText(search_results_text, query))  # Pass string to processText
