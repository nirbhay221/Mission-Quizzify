import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('tasks'))
for path in sys.path:
    print(path)
from task_3.task_3 import DocumentProcessor
from task_4.task_4 import EmbeddingClient
from task_5.task_5 import ChromaCollectionCreator

import os
from dotenv import load_dotenv

load_dotenv()

f"""
Task: Build a Quiz Builder with Streamlit and LangChain

Components to Integrate:
- DocumentProcessor: A class developed in Task 3 for processing uploaded PDF documents.
- EmbeddingClient: A class from Task 4 dedicated to embedding queries.
- ChromaCollectionCreator: A class from Task 5 responsible for creating a Chroma collection derived from the processed documents.

"""

if __name__ == "__main__":
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": os.getenv("PROJECT_NAME"),
        "location": "us-east1"
    }
    
    screen = st.empty() # Screen 1, ingest documents
    with screen.container():
        st.header("Quizzify")

        # 1) Initalize DocumentProcessor and Ingest Documents from Task 3
        # 2) Initalize the EmbeddingClient from Task 4 with embed config
        # 3) Initialize the ChromaCollectionCreator from Task 5

        processor = DocumentProcessor()
        processor.ingest_documents()
        
        embed_client = EmbeddingClient(**embed_config)
        
        chroma_creator = ChromaCollectionCreator(processor, embed_client)


        
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            # 4) Use streamlit widgets to capture the user's input
            # 4) for the quiz topic and the desired number of questions

            topic_input = st.text_input("Enter the Topic for the Quiz")
            num_questions = st.slider("Enter the number of quetions",min_value = 1,max_value = 10,step = 1, value = 5)

            document = None
            
            submitted = st.form_submit_button("Generate a Quiz!")
            if submitted:
                # 5) Use the create_chroma_collection() method to create a Chroma collection from the processed documents
                    
                chroma_collection = chroma_creator.create_chroma_collection()
                document = chroma_creator.query_chroma_collection(topic_input) 
                
    if document:
        screen.empty() # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document)