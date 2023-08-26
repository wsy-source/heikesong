from typing import Any
from langchain.tools import BaseTool
import requests

from services.SummaryServices import SummaryServices


class SummaryTool(BaseTool):
    name = "SummaryTool"
    description = """useful tool summary article 
                     This tool should only be used if the user question involves summary
                        parameter: file_name
                    """

    def _run(self, file_name: str) -> Any:
        article = SummaryServices.summary_article(file_name)
        return article

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        pass
