import streamlit as st
import requests
import os
from pathlib import Path

st.title("🔍 JFK Document Search")

# Initialize session state for results and selected document
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'selected_document' not in st.session_state:
    st.session_state.selected_document = None

# Function to read markdown file
def read_markdown_file(filename):
    documents_path = Path("./documents")
    file_path = documents_path / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def handle_document_click(filename):
    st.session_state.selected_document = filename

query = st.text_input("Enter your search query:")
if st.button("Search") and query:  # Only search if there's a query
    try:
        response = requests.post(
            "http://127.0.0.1:8000/search", 
            json={"query": query},
            timeout=30
        )
        
        response.raise_for_status()
        
        results = response.json()["results"]
        if results:
            st.session_state.search_results = results
        else:
            st.info("No results found for your query.")
            st.session_state.search_results = []
            
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display results and document content
if st.session_state.search_results:
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Search Results")
        for result in st.session_state.search_results:
            filename = result['filename']
            if st.button(f"📄 {filename}", key=filename):
                handle_document_click(filename)
    
    with col2:
        if st.session_state.selected_document:
            st.subheader(f"Document Content")
            content = read_markdown_file(st.session_state.selected_document)
            st.markdown(content)
