import os

from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

#
os.environ["OPENAI_API_TYPE"] = "Azure"
os.environ["OPENAI_API_KEY"] = "98e1aac5e1554c8db95b89e266c07177"
os.environ["OPENAI_API_BASE"] = "https://sean-aoai-gpt4.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
deployment_name = os.getenv("DEPLOYMENT_NAME", "gpt-4-32k")

llm = AzureChatOpenAI(deployment_name=deployment_name, request_timeout=20)

llm_embedding = OpenAIEmbeddings(openai_api_version="2023-03-15-preview",
                                 openai_api_key="705dd30eb44b4e3690c0fef2646d0628",
                                 openai_api_base="https://ms-build-china-aoai1.openai.azure.com/",
                                 openai_api_type="azure", chunk_size=1)
