import streamlit as st
import requests

st.title("🔍 JFK Document Search")

query = st.text_input("Enter your search query:")
if st.button("Search"):
    response = requests.post("http://127.0.0.1:8000/search", json={"query": query})
    
    if response.status_code == 200:
        results = response.json()["results"]
        for result in results:
            st.write(f"📄 **{result['filename']}**")
    else:
        st.error("Error fetching results")
