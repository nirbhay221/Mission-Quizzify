import streamlit as st
import os
import sys
import json
sys.path.append(os.path.abspath('tasks'))
from task_3.task_3 import DocumentProcessor
from task_4.task_4 import EmbeddingClient
from task_5.task_5 import ChromaCollectionCreator
from task_8.task_8 import QuizGenerator
from task_9.task_9 import QuizManager

import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": os.getenv("PROJECT_NAME"),
        "location": "us-central1"
    }
    # Add Session State
    if 'question_bank' not in st.session_state or len(st.session_state['question_bank']) == 0:
        
        # Step 1: init the question bank list in st.session_state
        if 'question_bank' not in st.session_state:
            st.session_state['question_bank'] = []
        if 'question_index' not in st.session_state:
            st.session_state['question_index'] = 0
        if 'display_quiz' not in st.session_state:
            st.session_state['display_quiz'] = False
        if 'input_type' not in st.session_state:
            st.session_state['input_type'] = None

        screen = st.empty()
        with screen.container():
            st.header("Quiz Builder")
            
            # Create a new st.form flow control for Data Ingestion
            with st.form(key = "input_form"):    
                input_type = st.selectbox(
                    label = "Select the type of input you want to upload",
                    options = ["PDF","DOCX","DOC","PPT","PPTX","Google Sheets","CSV","Notes","URL"]
                )
                select_submit_button = st.form_submit_button(label = "Submit")
                if select_submit_button:
                    st.session_state['input_type'] = input_type
                    st.rerun()
            
            if st.session_state['input_type']:       
                processor = DocumentProcessor()
                processor.ingest_documents(st.session_state['input_type'])
               
                embed_client = EmbeddingClient(**embed_config) 
            
                chroma_creator = ChromaCollectionCreator(processor, embed_client)
                
                # Step 2: Set topic input and number of questions
                
                topic_input = st.text_input("Enter the Topic for the Quiz")
                questions = st.slider("Enter the number of questions",min_value = 1,max_value = 10,step = 1, value = 5)    
                with st.form(key="quiz_form"):
                    submitted_part_2 = st.form_submit_button("Submit")
                    if submitted_part_2:
                        chroma_creator.create_chroma_collection()
                            
                        if len(processor.pages) > 0:
                            st.write(f"Generating {questions} questions for topic: {topic_input}")
                        
                        generator = QuizGenerator(topic_input, questions, chroma_creator.db)# Step 3: Initialize a QuizGenerator class using the topic, number of questrions, and the chroma collection
                        question_bank = generator.generate_quiz()
                        st.session_state['question_bank'] = question_bank
                        # Step 4: Initialize the question bank list in st.session_state
                        st.session_state["display_quiz"] = True
                        # Step 5: Set a display_quiz flag in st.session_state to True
                        st.session_state['question_index'] = 0
                        # Step 6: Set the question_index to 0 in st.session_state
                        st.rerun()

    elif st.session_state["display_quiz"]:
        
        st.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            quiz_manager = QuizManager(st.session_state['question_bank'])
            
            # Format the question and display it
            with st.form("MCQ"):
                # Step 7: Set index_question using the Quiz Manager method get_question_at_index passing the st.session_state["question_index"]
                index_question = quiz_manager.get_question_at_index(st.session_state['question_index'])
                
                # Unpack choices for radio button
                choices = []
                for choice in index_question['choices']:
                    key = choice['key']
                    value = choice['value']
                    choices.append(f"{key}) {value}")
                
                # Display the Question
                st.write(f"{st.session_state['question_index'] + 1}. {index_question['question']}")
                answer = st.radio(
                    "Choose an answer",
                    choices,
                    index = None
                )
                
                answer_choice = st.form_submit_button("Submit")
                
                # Step 8: Use the example below to navigate to the next and previous questions
                # Here we use the next_question_index method from our quiz_manager class
                st.form_submit_button("Next Question", on_click=lambda: quiz_manager.next_question_index(direction=1))
                
                st.form_submit_button("Previous Question", on_click=lambda: quiz_manager.next_question_index(direction=-1))
                
                if answer_choice and answer is not None:
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")
                    st.write(f"Explanation: {index_question['explanation']}")