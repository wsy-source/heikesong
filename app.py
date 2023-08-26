import json

from flask import Flask, request, jsonify, session
from langchain import PromptTemplate

from llm.llm import llm
from services.Classification import Classification
from services.ExtractionServices import ExtractionServices
from services.KeyWordRecommendationServices import KeyWordRecommendationServices
import logging
from services.ChiChatServices import ChiChat
from services.LoadDataService import LoadDataService
from services.SearchDocumentService import SearchDocument
from services.SummaryServices import SummaryServices
from services.AnalysisServices import AnalysisFile
from services.ArticleOverviewServices import ArticleOverviewServices
from util.TempStore import TempStore
from prompt.classification import CLASSIFICATION_PROMPT
from services.ChatServices import ChatService
from services.QuestionAndServices import QuestionAndAnswer
from util.util import addArticles, searchArticles

app = Flask(__name__)

content = ""


# app.secret_key = 'QWERTYUIOP'


@app.post("/keyword/recommendation")
def keyword_recommendation():
    try:
        args = request.get_json()
        topic = args["topic"]
        keywords = KeyWordRecommendationServices.recommend_keywords(topic)
        logging.info("get keywords: " + keywords)
        list_keyword = keywords.split(",")
    except Exception as e:
        error_message = e.__str__()
        return jsonify({"code": 500, "message": error_message})
    return jsonify({"code": 200, "message": list_keyword})


@app.post("/document/summarize")
def summarize():
    data = request.get_json()
    file_name = data["file_name"]
    article = SummaryServices.summary_article(file_name)
    print(article)
    return article


@app.route('/file/upload', methods=["POST"])
def addDocument():
    bodyInfo = request.get_json()
    title = bodyInfo['title']
    author = bodyInfo['author']
    doi = bodyInfo['doi']
    url = bodyInfo['url']
    user_id = bodyInfo['user_id']
    file_name = bodyInfo["file_name"]
    if not title:
        return {"code": 400, "Msg": "Missing title parameter"}
    elif not author:
        return {"code": 400, "Msg": "Missing author parameter"}
    elif not doi:
        return {"code": 400, "Msg": "Missing doi parameter"}
    elif not url:
        return {"code": 400, "Msg": "Missing url parameter"}
    elif not user_id:
        return {"code": 400, "Msg": "Missing user_id parameter"}

    # 文件信息提交不存摘要，AI摘要WSY识别完存，对话框上传要存摘要
    else:
        container_name = None
        try:
            container_name = bodyInfo["container_name"]
        except Exception as e:
            pass
        key, error = AnalysisFile.analysis_file(file_name, doi, container_name)
        if key == True:
            abstract = ""
            return addArticles(title, author, doi, url, user_id, abstract)
        else:
            return {"code": 500, "message": error}




@app.post("/search/documents")
def search_documents():
    data = request.get_json()
    question = data["question"]
    doi = data["doi"]
    content = SearchDocument.search_document(question=question, index_name=doi)
    return jsonify({"code": 200, "message": content["output_text"]})


@app.post("/article/overview/analysis")
def article_overview():
    data = request.get_json()
    content = data["content"]
    type = data["type"]
    if type == "analysis":
        content = ArticleOverviewServices.analysis_article(content)
    if type == "translate":
        content = ArticleOverviewServices.translate_article(content)
    return jsonify({"code": 200, "message": content})


# @app.post("/chat")
# def chat():
#     json = request.get_json()
#     question = json["question"]
#     result = ChatService.answer_question(question=question)
#     return {"code": 200, "message": result}

@app.post("/chat")
def chat2():
    data = request.get_json()
    question = data["question"]
    type = Classification.class_type(question)
    result = ""
    try:
        if type == "Summary":
            result = SummaryServices.summary_article(TempStore.content)
        if type == "Extract":
            result = ExtractionServices.extract_entity(TempStore.content)
        if type == "LoadData":
            # try:
            result = LoadDataService.load_data(question)
            # except Exception as e:
            #     result = "文件下载失败请检查DOI"
            #     pass
        if type == "Assistant":
            result = QuestionAndAnswer.answer_question_with_data(question=question, content=TempStore.content)
        if type == "Any":
            result = ChiChat.chat(question=question)
    except Exception as e:
        return {"code": 500, "message": e.__str__()}
    return {"code": 200, "message": result}


@app.post("/classfication")
def classfiy():
    data = request.get_json()
    question = data["question"]
    from langchain.chains import LLMChain
    prompt = PromptTemplate.from_template(CLASSIFICATION_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    return chain.run(question)


@app.route('/searchDocument', methods=["POST"])
def searchDocument():
    bodyInfo = json.loads(request.get_data(), strict=False)
    title = bodyInfo.get('title', None)
    author = bodyInfo.get('author', None)
    abstract = bodyInfo.get('abstract', None)
    return searchArticles(title, author, abstract)


#
# @app.post("/chat")
# def ChatData():


# @app.post("/article/overview/translate")
# def translate_file():
#     data = request.get_json()
#     content = data["content"]
#     content = ArticleOverviewServices.translate_article(content)
#     return jsonify({"code": 200, "message": content})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
