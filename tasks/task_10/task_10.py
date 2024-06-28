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
    if 'question_bank' not in st.session_state or len(st.session_state['question_bank']) == 0:
        
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
            with st.form(key = "input_form"):    
                input_type = st.selectbox(
                    label = "Select the type of input you want to upload",
                    options = ["PDF","DOCX","DOC","PPT","PPTX","Google Sheets","CSV","TXT","VIDEO_URL","URL","Excel"]
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
                
                
                topic_input = st.text_input("Enter the Topic for the Quiz")
                questions = st.slider("Enter the number of questions", min_value=1, max_value=10, step=1, value=5)    
                with st.form(key="quiz_form"):
                    submitted_part_2 = st.form_submit_button("Submit")
                    if submitted_part_2:
                        chroma_creator.create_chroma_collection()
                            
                        if len(processor.pages) > 0:
                            st.write(f"Generating {questions} questions for topic: {topic_input}")
                        
                        generator = QuizGenerator(topic_input, questions, chroma_creator.db)
                        question_bank = generator.generate_quiz()
                        st.session_state['question_bank'] = question_bank
                        st.session_state["display_quiz"] = True
                        st.session_state['question_index'] = 0
                        st.rerun()

    elif st.session_state["display_quiz"]:
        
        st.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            quiz_manager = QuizManager(st.session_state['question_bank'])
            
            with st.form("MCQ"):
                index_question = quiz_manager.get_question_at_index(st.session_state['question_index'])
                
                st.write("Debug: index_question['choices']", index_question['choices'])
                
                choices = []
                for choice in index_question['choices']:
                    if isinstance(choice, dict) and 'key' in choice and 'value' in choice:
                        key = choice['key']
                        value = choice['value']
                        choices.append(f"{key}) {value}")
                    else:
                        st.error("Error: Choice structure is incorrect.")
                        st.stop()
                
                st.write(f"{st.session_state['question_index'] + 1}. {index_question['question']}")
                answer = st.radio(
                    "Choose an answer",
                    choices,
                    index=None
                )
                
                answer_choice = st.form_submit_button("Submit")
                
                st.form_submit_button("Next Question", on_click=lambda: quiz_manager.next_question_index(direction=1))
                st.form_submit_button("Previous Question", on_click=lambda: quiz_manager.next_question_index(direction=-1))
                
                if answer_choice and answer is not None:
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")
                    st.write(f"Explanation: {index_question['explanation']}")
