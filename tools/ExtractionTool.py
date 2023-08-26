import os
from typing import Any

from langchain import PromptTemplate
from langchain.document_loaders import AzureBlobStorageFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.tools import BaseTool
import requests
from langchain.chains import LLMChain

from llm.llm import llm
from prompt.Extraction import EXTRACTION_PROMPT
from services.ExtractionServices import ExtractionServices
from services.SummaryServices import SummaryServices


class ExtractionTool(BaseTool):
    name = "ExtractionTool"
    description = """useful tool extract article's conceptual entity 
                     This tool should only be used if the user question involves extraction
                        parameter: file_name
                    """

    def _run(self, file_name: str) -> Any:
        conn_string = os.getenv("STORAGE_CONNECTION_STRING",
                                "DefaultEndpointsProtocol=https;AccountName=cggptsc;AccountKey=rWvHP0XV8ji7QnVDDASpbjApgiixQ/RITbzlF62z7CWPkIXWzi6W5ZJIlf0UXU5/Eg5UTwx13XaB+AStuckFbQ==;EndpointSuffix=core.windows.net")
        container_name = os.getenv("CONTAINER_NAME", "gptfiles")
        blob_loader = AzureBlobStorageFileLoader(conn_str=conn_string, container=container_name,
                                                 blob_name=file_name)
        prompt = PromptTemplate.from_template(EXTRACTION_PROMPT)
        splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        documents = blob_loader.load_and_split(splitter)
        chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
        results = []
        for document in documents:
            result = chain.run(document.page_content)
            results.append(result)
        result = chain.run(str(results))
        return result

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        pass
