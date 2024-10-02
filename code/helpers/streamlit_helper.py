import streamlit as st
from dotenv import load_dotenv
import os

def init_page(title:str):
	load_dotenv()

	azure_search_service : str = os.getenv("AZURE_SEARCH_SERVICE") or ""
	azure_search_key : str = os.getenv("AZURE_SEARCH_KEY") or ""
	storage_connection_string : str = os.getenv("AZURE_BLOB_CONNECTION_STRING") or ""

	st.set_page_config(page_title="MTC Ingestor for RAG", page_icon=os.path.join('images','favicon.ico'), layout="wide", menu_items=None)
	st.sidebar.title("RAG Ingestor", anchor="center")
	st.sidebar.image(os.path.join('images','ingestor-logo.png'), use_column_width=True)
	st.sidebar.image(os.path.join('images','logo-ms.png'), use_column_width=True)
	st.sidebar.divider()
	st.session_state["blob_connstring"] = st.sidebar.text_input("Blob Connectionstring", storage_connection_string)
	st.session_state["ai_search_endpoint"] = st.sidebar.text_input("AI Search endpoint", azure_search_service)
	st.session_state["ai_search_key"] = st.sidebar.text_input("AI Search key", azure_search_key, type="password")
	st.markdown(f"### {title}")