from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

context_str='''
economy in the world. New York City is an established safe haven for global investors. New York is home to the highest number of billionaires, individuals of ultra-high net worth (greater than US$30 million), and millionaires of any city in the world.
busiest pedestrian intersections and a major center of the world's entertainment industry. Many of the city's landmarks, skyscrapers, and parks are known around the world, and the city's fast pace led to the phrase New York minute. The Empire State Building is a global standard of reference to describe the height and length of other structures.Manhattan's real estate market is among the most expensive in the world. Providing continuous 24/7 service and contributing to the nickname The City That
The city and its metropolitan area constitute the premier gateway for legal immigration to the United States. As many as 800 languages are spoken in New York, making it the most linguistically diverse city in the world. New York City is home to more than 3.2 million residents born outside the U.S., the largest foreign-born population of any city in the world as of 2016.New York City traces its origins to a trading post founded on the southern tip of Manhattan Island by Dutch colonists in
approximately 1624. The settlement was named New Amsterdam (Dutch: Nieuw Amsterdam) in 1626 and was chartered as a city in 1653. The city came under British control in 1664 and was renamed New York after King Charles II of England granted the lands to his brother, the Duke of York. The city was regained by the Dutch in July 1673 and was renamed New Orange for one year and three months; the city has been continuously named New York since November 1674. New York City was the capital of the United
'''
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n{context}\n\nQuestion: {question}\nHelpful Answer:"""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="tinyllama")

chain = prompt | model

print(chain.invoke({"question":"What is the economic significance of New York City?","context": context_str}))
