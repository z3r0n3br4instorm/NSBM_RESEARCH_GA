import spacy

# Load a pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

def extract_context_and_topic(prompt):
    """
    Extracts the main topic from the prompt for targeted searches.
    """
    # Step 1: Process the text
    doc = nlp(prompt)

    # Step 2: Extract potential keywords (technical terms, proper nouns, etc.)
    keywords = [token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop]

    # Step 3: Normalize and identify core topics (example: distributed systems)
    # Predefined topics or domains
    topics = ["distributed systems", "networking", "cloud computing", "databases"]

    # Find relevant topics based on extracted keywords
    for topic in topics:
        if any(word in topic for word in keywords):
            return topic, keywords

    # Default fallback if no specific topic is matched
    return "general topic", keywords

# Example usage
prompt = "What is NSBM and where is it located?"
topic, keywords = extract_context_and_topic(prompt)

print("Detected Topic for Search:", topic)
print("Extracted Keywords:", keywords)
