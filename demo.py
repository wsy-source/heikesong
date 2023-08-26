import asyncio
import datetime
import os

import tiktoken
from langchain import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import AzureBlobStorageFileLoader
from langchain.chains import APIChain
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from llm.llm import llm
from prompt.Extraction import EXTRACTION_PROMPT, REFINE_PROMPT
from langchain.chains import LLMChain

from prompt.summary import SUMMARY_PROMPT, SUMMARY_PROMPT2
filename = "main.pdf"
conn_string = os.getenv("STORAGE_CONNECTION_STRING",
                        "DefaultEndpointsProtocol=https;AccountName=cggptsc;AccountKey=rWvHP0XV8ji7QnVDDASpbjApgiixQ/RITbzlF62z7CWPkIXWzi6W5ZJIlf0UXU5/Eg5UTwx13XaB+AStuckFbQ==;EndpointSuffix=core.windows.net")
container_name = os.getenv("CONTAINER_NAME", "gptfiles")
blob_loader = AzureBlobStorageFileLoader(conn_str=conn_string, container=container_name,
                                         blob_name=filename)
encoding = tiktoken.get_encoding("gpt2")
splitter = CharacterTextSplitter()
document = blob_loader.load_and_split(splitter)
question_prompt = PromptTemplate.from_template(SUMMARY_PROMPT2)
format_prompt = question_prompt.format_prompt(input_documents=str(document))
num_tokens = len(encoding.encode(format_prompt.to_string()))
print(num_tokens)
while num_tokens > 27000:
    document.pop()
    question_prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
    format_prompt = question_prompt.format_prompt(input_documents=str(document))
    num_tokens = len(encoding.encode(format_prompt.to_string()))
    print(num_tokens)


chain = LLMChain(llm=llm, prompt=question_prompt, verbose=True)
print(chain.run(str(document)))
