import spacy
import sqlite3
import requests
from bs4 import BeautifulSoup


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


class WebRag_Engine:
    def __init__(self):
        self.researchWebsites = [
            "https://www.wikipedia.org",
            "https://www.bbc.co.uk",
            "https://www.nsbm.ac.lk",
            "https://www.google.com",
            "https://www.youtube.com",
        ]

    def retrieveData(self, query):
        # Normalize the query for basic text matching
        query_terms = [term.lower() for term in query.split()]
        results = []

        for website in self.researchWebsites:
            try:
                response = requests.get(website, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    paragraphs = soup.find_all("p")  # Extract all paragraphs

                    for paragraph in paragraphs:
                        paragraph_text = paragraph.get_text().strip().lower()
                        if any(term in paragraph_text for term in query_terms):
                            results.append(
                                f"Relevant text found on {website}:\n{paragraph.get_text().strip()}\n"
                            )
                else:
                    results.append(f"Could not access {website}.")
            except requests.RequestException as e:
                results.append(f"Error accessing {website}: {e}")

        return results if results else ["No relevant data found."]

if __name__ == "__main__":
    topics = ["Artificial Intelligence", "Machine Learning", "Natural Language Processing"]
    query = "What is the impact of artificial intelligence on modern businesses?"

    web_rag = WebRagEngine(topics)
    for result in web_rag.retrieveData(query):
        print(result)