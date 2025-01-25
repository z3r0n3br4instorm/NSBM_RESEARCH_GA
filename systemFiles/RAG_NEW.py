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
#----

class RAG_Engine:
    def __init__(self, target):
        self.targetModelName = target
        self.targetLLM = Ollama(model=self.targetModelName, base_url="http://127.0.0.1:11434")
        self.embedder = OllamaEmbeddings(model = self.targetModelName, base_url='http://127.0.0.1:11434')


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
        response = retrieval_chain.invoke({"input": prompt})
        return response



# class RAG_Engine:
#     def __init__(self, topics):
#         self.nlp = spacy.load("en_core_web_sm")
#         self.topics = topics
#         self.RagEngine = False
#         self.topic = None
#         self.keywords = None
#         self.matching_topics = []

#     def retrieveData(self, query, topics):
#         self.matching_topics = []
#         self.doc = self.nlp(query)
#         self.keywords = [
#             token.text.lower()
#             for token in self.doc
#             if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop
#         ]
#         self.topics = topics

#         for self.topic in self.topics:
#             if any(word in self.topic for word in self.keywords):
#                 self.matching_topics.append(self.topic)

#         return self.matching_topics if self.matching_topics else ["General Topic"]

#     def runPrompt(self, prompt):
#         matching_topics = self.retrieveData(prompt, self.topics)
#         if matching_topics == ["General Topic"]:
#             self.RagEngine = False
#         else:
#             self.RagEngine = True

#     def ragResearchOn(self, sourceDB):
#         if self.RagEngine:
#             print(f"Research Engine is Running on topics: {self.matching_topics}")
#             conn = sqlite3.connect(sourceDB)
#             cursor = conn.cursor()
#             results = []

#             for topic in self.matching_topics:
#                 try:
#                     table_name = topic.replace(" ", "_")
#                     cursor.execute(f"SELECT * FROM {table_name}")
#                     rows = cursor.fetchall()

#                     if rows:
#                         for row in rows:
#                             results.append(
#                                 f"ID: {row[0]}, Contexts: {row[1]}, About: {row[2]}, Overall: {row[3]}"
#                             )
#                     else:
#                         results.append(f"No data found for topic: {topic}")
#                 except sqlite3.OperationalError:
#                     results.append(
#                         f"Table for topic '{topic}' does not exist in the database."
#                     )

#             conn.close()
#             if results:
#                 return results
#             else:
#                 return ["No research data found."]
#         else:
#             return None


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
    query = "What is NSBM Green University?"

    web_rag = WebRag_Engine().retrieveData(query)
    # for result in web_rag.retrieveData(query):
    #     print(result)
    print(web_rag)
    #
    # New Implementation
    rag = RAG_Engine("tinyllama")
    print(rag.processText("\n".join(web_rag), query))
