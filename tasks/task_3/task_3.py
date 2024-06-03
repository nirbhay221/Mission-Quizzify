# pdf_processing.py

# Necessary imports
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,UnstructuredPowerPointLoader, TextLoader, UnstructuredExcelLoader, WebBaseLoader
import os
import tempfile
import sys
import uuid
import os
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader,PlaywrightURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi

print(sys.path)

load_dotenv()

class Document:
    def __init__(self, page_content='',metadata = None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}
        
    def __str__(self):
        return f"Document(page_content='{self.page_content}', metadata={self.metadata})"
        
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
            self.process_docx()
        if input_type == "PPT":
            self.process_pptx()
        if input_type == "PPTX":
            self.process_pptx()
        if input_type == "Google Sheets":
            self.process_googleSheets()
        if input_type == "VIDEO_URL":
            self.process_video_url()
        if input_type == "URL":
            self.process_url()
        if input_type == "CSV":
            self.process_csv()
        if input_type == "TXT":
            self.process_txt()
        if input_type == "Excel":
            self.process_xlsx()
                
    def process_pdf(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit PDF Uploader",
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
                print("---------------DOCS-------------",docs)
                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                pages.extend(docs)
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
            self.pages = pages
            
            
            
    def process_xlsx(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit Excel Uploader",
            accept_multiple_files= True,
            type = ["xlsx"]
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
                loader = UnstructuredExcelLoader(temp_file_path)
                docs = loader.load()
                print("---------------DOCS-------------",docs)
                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                pages.extend(docs)
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
            self.pages = pages
            
            
            
            
            
            
    def process_txt(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit TXT Uploader",
            accept_multiple_files= True,
            type = ["txt"]
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
                loader = TextLoader(temp_file_path)
                docs = loader.load()
                print("---------------DOCS-------------",docs)
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
                label = "Streamlit CSV Uploader",
                accept_multiple_files= True,
                type = ["csv"]
            )
            
            if uploaded_files is not None:
                pages = []
                for uploaded_file in uploaded_files:
                    # Generate a unique identifier to append to the file's original name
                    unique_id = uuid.uuid4().hex
                    original_name, file_extension = os.path.splitext(uploaded_file.name)
                    temp_file_name = f"{original_name}_{unique_id}{file_extension}"
                    temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)

                    with open(temp_file_path, 'wb') as f:
                    # Write the uploaded PDF to a temporary file
                        f.write(uploaded_file.getvalue())

                    # Step 2: Process the temporary file
                    #####################################
                    loader = CSVLoader(temp_file_path)
                    docs = loader.load()

                    # Step 3: Then, Add the extracted pages to the 'pages' list.
                    #####################################
                    pages.extend(docs)
                    # Clean up by deleting the temporary file.
                    os.unlink(temp_file_path)
                
                # Display the total number of pages processed.
                st.write(f"Total pages processed: {len(self.pages)}")
                self.pages = pages


    def process_url(self):
            urls_input = st.text_area("Enter URLs separated by comma (,)")
            urls = [url.strip() for url in urls_input.split(",") if url.strip()]
            
            if urls is not None:
                pages = []
                for url in urls:
                    try:    
                        loader = WebBaseLoader(url)
                        loader.request_kwargs = {'verify': False}
                        
                        docs = loader.load()
                    except Exception as e : 
                        st.write(f"Web Base Loader failed for {url} with error {str(e)}")
                        try:
                            loader = UnstructuredURLLoader(urls = [url])
                            docs = loader.load()
                        except Exception as e:
                            st.write(f"Unstructured URL Loader failed for {url} with error: {str(e)}")
                            try:
                                loader = PlaywrightURLLoader(urls = [url])
                                docs = loader.load()
                            except Exception as e:
                                st.write(f"Unstructured URL Loader failed for {url} with error: {str(e)}")
                                

                    pages.extend(docs)
                
                st.write(f"Total pages processed: {len(self.pages)}")
                self.pages = pages



                
    def process_docx(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit DOCX Uploader",
            accept_multiple_files= True,
            type = ["docx","doc"]
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
                loader = Docx2txtLoader(temp_file_path)
                docs = loader.load()
                print("---------------DOCS-------------",docs)
                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                pages.extend(docs)
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
            self.pages = pages

        
    def process_pptx(self):

        uploaded_files = st.file_uploader(
            label = "Streamlit PPTX Uploader",
            accept_multiple_files= True,
            type = ["pptx","ppt"]
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
                loader = UnstructuredPowerPointLoader(temp_file_path)
                docs = loader.load()
                print("---------------DOCS-------------",docs)
                # Step 3: Then, Add the extracted pages to the 'pages' list.
                #####################################
                pages.extend(docs)
                # Clean up by deleting the temporary file.
                os.unlink(temp_file_path)
            
            # Display the total number of pages processed.
            st.write(f"Total pages processed: {len(self.pages)}")
            self.pages = pages



    def process_video_url(self):
        video_url = st.text_input("Enter Video URL", "")
        
        
        if video_url:
            
            video_id = video_url.split("v=")[1].split("&")[0]
            print(f'----------------LINK ID------------{video_id}')
            metadata = {'video_id': video_id}
            
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            timestamps = [entry['start'] for entry in transcript]
            selected_timestamp = st.slider("Select Timestamp", min_value=0, max_value=len(timestamps)-1)
            selected_entry = transcript[selected_timestamp]
            start_time = selected_entry['start']
            end_time = start_time + selected_entry['duration']
            transcript_content = ""
            docs = []
            
            pages = []
            i = 0
            for entry in transcript:
                if entry['start'] >= start_time and entry['start'] <= end_time:
                    words = entry['text'].split()
                    formatted_text = "\\n".join(words) 
                    metadata = {
                        'page' : i
                    }
                    transcript_content += formatted_text + " "
                    docs = [Document(page_content=transcript_content,metadata=metadata)]
                    
                    i+=1
                    pages.extend(docs)
            print(pages)
            
            # print(video_url)
            # loader = YoutubeLoader.from_youtube_url(video_url,add_video_info=True)
            # docs = loader.load()
            # print("-----------------------DOCS---------------------",docs)
            # # Add extracted pages to the 'pages' list
            
            # Display the total number of pages processed
            st.write(f"Total pages processed: {len(pages)}")
            self.pages = pages




if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents("PDF")
