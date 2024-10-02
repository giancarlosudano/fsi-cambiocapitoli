from math import e
import yaml
import os

def read_file(file_path):
	with open(file_path, "r") as file:
		return file.read()

def count_all_markdown_files(folder):
	i = 0
	for dirpath, dirnames, filenames in os.walk(folder):
		for filename in filenames:
			if filename.endswith('.md'):
				i += 1
	return i


def count_all_files_with_extensions(folder, extension):
	i = 0
	for dirpath, dirnames, filenames in os.walk(folder):
		for filename in filenames:
			if filename.endswith(extension):
				i += 1
	return i

def count_all_files(folder):
	i = 0
	for dirpath, dirnames, filenames in os.walk(folder):
		for filename in filenames:
				i += 1
	return i

def count_non_markdown_files(directory):
	i = 0
	# Walk through all directories and files in the provided directory
	for dirpath, dirnames, files in os.walk(directory):
		for file in files:
			if not file.endswith('.md'):
				i += 1
	return i

def extract_yaml_front_matter(content: str):
	
	# Cerca l'inizio e la fine del front matter YAML
	start = content.find('---') + 3
	end = content.find('---', start)
	
	# Verifica se il front matter è stato trovato
	if start != -1 and end != -1:
		yaml_content = content[start:end]
		try:
			# Prova ad analizzare il contenuto YAML
			data = yaml.safe_load(yaml_content)
			return data
		except yaml.YAMLError as error:
			print(f"Errore durante l'analisi YAML: {error}")
			return {}
	else:
		# Front matter non trovato
		return {}

