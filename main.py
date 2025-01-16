# Prototype Program For GA Core

import sqlite3
import spacy
from ollama import chat

global version
version = "0.0.1"


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


class RAG_Engine:
    def __init__(self, topics):
        self.nlp = spacy.load("en_core_web_sm")
        self.topics = topics
        self.RagEngine = False
        self.topic = None
        self.keywords = None
        self.matching_topics = []

    def retrieveData(self, query, topics):
        self.matching_topics = []
        self.doc = self.nlp(query)
        self.keywords = [
            token.text.lower()
            for token in self.doc
            if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop
        ]
        self.topics = topics

        for self.topic in self.topics:
            if any(word in self.topic for word in self.keywords):
                self.matching_topics.append(self.topic)

        return self.matching_topics if self.matching_topics else ["General Topic"]

    def runPrompt(self, prompt):
        matching_topics = self.retrieveData(prompt, self.topics)
        if matching_topics == ["General Topic"]:
            self.RagEngine = False
        else:
            self.RagEngine = True

    def ragResearchOn(self, sourceDB):
        if self.RagEngine:
            print(f"Research Engine is Running on topics: {self.matching_topics}")
            conn = sqlite3.connect(sourceDB)
            cursor = conn.cursor()
            results = []

            for topic in self.matching_topics:
                try:
                    table_name = topic.replace(" ", "_")
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    if rows:
                        for row in rows:
                            results.append(
                                f"ID: {row[0]}, Contexts: {row[1]}, About: {row[2]}, Overall: {row[3]}"
                            )
                    else:
                        results.append(f"No data found for topic: {topic}")
                except sqlite3.OperationalError:
                    results.append(
                        f"Table for topic '{topic}' does not exist in the database."
                    )

            conn.close()
            if results:
                return results
            else:
                return ["No research data found."]
        else:
            return None


# class WebScraperEngine:

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
        ragContext = rag.ragResearchOn("GADB.db")
        if ragContext != None:
            prompt = f"""$$DATA_FROM_RAG_ENGINE:\n{ragContext}
                        \nDATA_FROM_RAG_ENGINE_END$$\n{prompt}
                    """
        print(f"{gamodel.runChat(prompt)}")
