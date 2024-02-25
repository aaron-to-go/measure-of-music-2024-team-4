from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA 
from langchain.document_loaders.csv_loader import CSVLoader
import os

def get_recommendations(project_description, openai_api_key):

    # Load the music data csv
    loader = CSVLoader(file_path="data.csv", encoding="utf-8", csv_args={
                'delimiter': ';'})
    data = loader.load()

    # Building a Vector DB For The Documents
    embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)
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
    query = """
    Objective: You are a music supervisor. You will receive a project description containing information about a commercial or video that the user needs music for.
    Your primary role is to recommend a fitting song from the context based on the provided project description.
Tasks:
1. Analyze the Description: Understand all aspects of the project based on the description. Think of the mood, key visuals, theme, target audience, duration and any specific thematic elements or narrative details. Note any specific requests or elements that the song must complement or enhance.
2. Song Selection: Based on the analysis, choose a song from the provided database that best fits the requirements. Consider tall aspects of the song that you have available, and overall vibe to ensure it matches the projects mood and objectives.
3. Justification: Provide a brief explanation for your song choice. Explain how the songs characteristics align with the project theme, mood, and target audience.
4. Spotify_Streams and popularity score to give a potential indication of price.
5. Suggest 3 songs in total using the instructions above.
6. Finally, give the user Feedback on what information could be needed to give better results
Guidelines:
- Ensure your recommendations are based on the description provided and relevant to the projects goals.
- The recommended songs must be from the context.
- Maintain a professional and informative tone throughout your response.
- Every suggestion you make, should contain the following information: 1.track name 2.artist 3.spotify_track_link as hyperlink 4.justification 5. spotify-streams and price indication.
- Format it in a nice and clear way
Project description: """ + project_description
    
    # Executing the RetreivalIQA model with the defined query. 
    result = recommendation_qa.run(query)

    return result
