# pdf_processing.py

# Necessary imports
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import os
import tempfile
import sys
import uuid
import os
from dotenv import load_dotenv

print(sys.path)

load_dotenv()
class DocumentProcessor:
    
    """
    This class encapsulates the functionality for processing uploaded PDF documents using Streamlit
    and Langchain's PyPDFLoader. It provides a method to render a file uploader widget, process the
    uploaded PDF files, extract their pages, and display the total number of pages extracted.
    """
    def __init__(self):
        self.pages = []  # List to keep track of pages from all documents
    
    def ingest_documents(self,input_type):
        """
        Renders a file uploader in a Streamlit app, processes uploaded PDF files,
        extracts their pages, and updates the self.pages list with the total number of pages.
        
        Given:
        - Handling of temporary files with unique names to avoid conflicts.
        """
        
        # Step 1: Render a file uploader widget. 
        st.title("Document Processor")
        
        if input_type == "PDF":
            self.process_pdf()
        if input_type == "DOCX":
            self.process_docx()
        if input_type == "DOC":
            self.process_doc()
        if input_type == "PPT":
            self.process_ppt()
        if input_type == "PPTX":
            self.process_pptx()
        if input_type == "Google Sheets":
            self.process_googleSheets()
        if input_type == "URL":
            self.process_url()
        if input_type == "Notes":
            self.process_notes()
                
    def process_pdf(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit Multiple PDF Uploader",
            accept_multiple_files= True,
            type = ["pdf"]
        )
        
        if uploaded_files is not None:
            pages = []
            for uploaded_file in uploaded_files:
                # Generate a unique identifier to append to the file's original name
                unique_id = uuid.uuid4().hex
                original_name, file_extension = os.path.splitext(uploaded_file.name)
                temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                # Write the uploaded PDF to a temporary file
                with open(temp_file_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())

                # Step 2: Process the temporary file
                #####################################
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()

                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                pages.extend(docs)
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
            self.pages = pages

    def process_csv(self):

            uploaded_files = st.file_uploader(
                label = "Streamlit Multiple PDF Uploader",
                accept_multiple_files= True,
                type = ["pdf"]
            )
            
            if uploaded_files is not None:
                pages = []
                for uploaded_file in uploaded_files:
                    # Generate a unique identifier to append to the file's original name
                    unique_id = uuid.uuid4().hex
                    original_name, file_extension = os.path.splitext(uploaded_file.name)
                    temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                    temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                    # Write the uploaded PDF to a temporary file
                    with open(temp_file_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())

                    # Step 2: Process the temporary file
                    #####################################
                    loader = PyPDFLoader(temp_file_path)
                    docs = loader.load()

                    # Step 3: Then, Add the extracted pages to the 'pages' list.
                    #####################################
                    pages.extend(docs)
                    # Clean up by deleting the temporary file.
                    os.unlink(temp_file_path)
                
                # Display the total number of pages processed.
                st.write(f"Total pages processed: {len(self.pages)}")
                self.pages = pages

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents("PDF")
