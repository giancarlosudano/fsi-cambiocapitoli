import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import traceback
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
import helpers.langchain_helper as lc_hlp
import helpers.azure_search_helper as search_hlp
import helpers.formatting_helper as fmt_hlp
import helpers.utility_helper as utl_hlp

def check_show_link(answer: str) -> bool:
	llm = lc_hlp.get_gpt(streaming=True, temperature=0.0)
	input_variables = ["testo"]
	prompt_text = utl_hlp.read_file(os.path.join("prompt","verify.txt"))
	prompt_template = PromptTemplate(template=prompt_text, input_variables=input_variables)
	chain = prompt_template | llm | StrOutputParser()
	generation = chain.invoke({"testo": answer})
	risposta = "true" in generation.lower()
	return risposta

try:
	load_dotenv()
	st.set_page_config(page_title="Chat con Poste Search", page_icon=os.path.join('images','favicon.ico'), layout="wide", menu_items=None)
	st.title("Chat con 'Poste Search'")
	st.sidebar.image(os.path.join('images','logo-poste.png'), use_column_width=True)

	if st.session_state['authentication_status']:
		pass
	elif not st.session_state['authentication_status']:
		st.warning('Username/password is incorrect')
		st.stop()
	elif st.session_state['authentication_status'] is None:
		st.warning('Please enter your username and password')
		st.stop()

	k = st.sidebar.slider("Pag. da recuperare?", value=5, min_value=3, max_value=20, step=1, key="k")
	parentdoc = st.sidebar.checkbox("Considera pagina intera", value=True)

	if st.sidebar.button("Nuova chat"):
		st.session_state.messages = []
		st.rerun()
	if "messages" not in st.session_state:
		st.session_state.messages = []

	for message in st.session_state.messages:
		if message["role"] == "assistant":
			with st.chat_message(message["role"], avatar=os.path.join('images','pt-avatar.png')):
				st.markdown(message["content"])
		else:
			with st.chat_message(message["role"]):
				st.markdown(message["content"])

	if question := st.chat_input("Chiedi informazioni al bot", key="chat_input"):
		
		with st.chat_message("user"):
			st.markdown(question)

		with st.spinner("ricerca informazioni..."):
			st.session_state.messages.append({"role": "user", "content": question})
			history_formatted = fmt_hlp.format_user_messages(st.session_state.messages)
			store_source = search_hlp.get_store(os.getenv("AZURE_SEARCH_INDEX_NAME"))
			
			chunks = store_source.similarity_search(query=history_formatted, k=k, search_type="hybrid")

			if parentdoc:
				source_urls, parents = search_hlp.get_parentdoc_from_chunks(chunks, container_name=os.getenv("AZURE_BLOB_CONTAINER_NAME"))
			
		with st.spinner("elaborazione risposta..."):
			llm = lc_hlp.get_gpt(streaming=True, temperature=0.0)
			input_variables = ["question", "context", "history"]
			prompt_text = utl_hlp.read_file(os.path.join("prompt","rag.txt"))
			prompt_template = PromptTemplate(template=prompt_text, input_variables=input_variables)
			chain = prompt_template | llm | StrOutputParser()

			if parentdoc:
				context = fmt_hlp.format_parents(parents)
			else:	
				context = fmt_hlp.format_chunks(chunks)
				
			generation = chain.invoke({"question": question ,"context": context, "history": fmt_hlp.format_all_messages(st.session_state.messages)})

			show_link = check_show_link(generation)

			with st.chat_message("assistant", avatar=os.path.join('images','pt-avatar.png')):
				st.markdown(generation)

				if show_link:
					unique_chunks = []
					for chunk in chunks:
						if chunk.metadata["source"] not in [c.metadata["source"] for c in unique_chunks]:
							unique_chunks.append(chunk)

					link_container = st.expander(label="link usati per generare la risposta", expanded=True)
		
					with link_container:
						for i, chunk in enumerate(unique_chunks):
							url = chunk.metadata["source"].replace(".md", ".html")
							description = chunk.metadata["title"]
							
							st.markdown(f'[{description}](http://{url})', unsafe_allow_html=True)

			st.session_state.messages.append({"role": "assistant", "content": generation})

except Exception:
	st.error(traceback.format_exc())