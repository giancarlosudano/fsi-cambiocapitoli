import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_gpt(streaming : bool = False, temperature : float = 0.0):
	azure_endpoint: str = os.getenv("AZURE_OPENAI_BASE") or ""
	api_key = os.getenv("AZURE_OPENAI_API_KEY") or ""
	api_version: str = os.getenv("AZURE_OPENAI_API_VERSION") or ""
	azure_openai_deployment : str = os.getenv("AZURE_OPENAI_MODEL") or ""
	llm = AzureChatOpenAI(azure_deployment=azure_openai_deployment, temperature=temperature, streaming=False, azure_endpoint=azure_endpoint, api_key=api_key, api_version=api_version)
	return llm