from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA 
from langchain.document_loaders.csv_loader import CSVLoader

def get_recommendations(project_description, openai_api_key):

    # Load the music data csv
    loader = CSVLoader(file_path="data.csv", encoding="utf-8", csv_args={
                'delimiter': ','})
    data = loader.load()

    embedding_function = OpenAIEmbeddings()


    # Building a Vector DB For The Documents
    vectordb = Chroma.from_documents(data, embedding_function)

    # Initializing the ChatGPT Model.
    llm = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key)

    # Creating a RetrivalIQA model combining the langauge model and vector database. 
    recommendation_qa = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(search_kwargs={'k': 4}),
        chain_type="stuff",
    )

    # Defining the Query. 
    query = """Objective: You are to function as a music supervisor for commercials. Your primary role is to recommend a fitting song from the database based on the project description of a commercial provided.
Tasks:
1. Analyze the Description: Understand all aspects of the commercial based on the description. Think of the mood, key visuals, theme, target audience, and any specific thematic elements or narrative details. Note any specific requests or elements that the song must complement or enhance.
2. Song Selection: Based on the analysis, choose a song from the provided database that best fits the commercials requirements. Consider the songs tempo, genre, lyrics (if applicable), and overall vibe to ensure it matches the commercials mood and objectives.
3. Justification: Provide a brief explanation for your song choice. Explain how the songs characteristics align with the commercials theme, mood, and target audience.
4. Alternative Options: Optionally, you may suggest up to two alternative songs from the database that could also fit the commercial. Briefly describe why these alternatives were considered and how they differ from your primary choice.
Guidelines:
Ensure your recommendations are based on the description provided and relevant to the commercials goals.
The song must be from the database.
Maintain a professional and informative tone throughout your response.
List the recommendations descending and use the song title and artist as the title.
Project description: """ + project_description
    
    # Executing the RetreivalIQA model with the defined query. 
    result = recommendation_qa.run(query)

    return result
