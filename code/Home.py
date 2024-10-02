import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import glob
from langchain import PromptTemplate, LLMChain
import helpers.langchain_helper as lc_hlp
import streamlit as st
import traceback
from dotenv import load_dotenv

try:
	load_dotenv()
	
	st.set_page_config(page_title="Cambio Stile", page_icon=os.path.join('images','favicon.ico'), layout="wide", menu_items=None)
	st.title("Cambio Stile")
	st.sidebar.write("Version 0.1.1")
	
	st.markdown("""Cambio stile documenti""")

	if st.button("Lancia processo"):
		st.write("Processo lanciato")
		llm = lc_hlp.get_gpt(streaming=True, temperature=0.0)

		# Definisci il prompt template
		prompt_template = """Sei un assistente di scrittura. Riscrivi considerevolmente il seguente paragrafo per cambiarne lo stile e la forma, ma senza cambiare il contenuto. Mantieni il titolo invariato.

		Titolo: {title}

		Paragrafo:
		{paragraph}

		Paragrafo Riscritto:"""

		prompt = PromptTemplate(
			input_variables=["title", "paragraph"],
			template=prompt_template,
		)

		# Crea la LLM chain
		chain = LLMChain(llm=llm, prompt=prompt)

		# Leggi i file di testo e processali
		input_folder = 'input_texts'
		output_file = 'output.txt'

		# Lista per conservare i paragrafi processati
		processed_paragraphs = []

		# Ottieni la lista dei file di testo nella cartella di input
		text_files = glob.glob(os.path.join(input_folder, '*.txt'))

		for file_path in text_files:
			with open(file_path, 'r', encoding='utf-8') as file:
				content = file.read()
				
				# Supponendo che il titolo sia la prima linea
				lines = content.strip().split('\n')
				title = lines[0]
				paragraph = '\n'.join(lines[1:])
				st.write(title)
				st.write(paragraph)
				st.write('\n\n')
				# Esegui la chain
				rewritten_paragraph = chain.run(title=title, paragraph=paragraph)
				st.write(rewritten_paragraph)
				st.write('==================================================')
				# Aggiungi alla lista
				processed_paragraphs.append(rewritten_paragraph)

		# Combina e salva il risultato
		final_output = '\n\n'.join(processed_paragraphs)

		with open(output_file, 'w', encoding='utf-8') as file:
			file.write(final_output)

except Exception:
	st.error(traceback.format_exc())