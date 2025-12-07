from langchain_openai import AzureChatOpenAI
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from src.prompt_template import get_prompt
from config.config import *

class AnimeRecommender:
    def __init__(self,retriever):
        self.llm = AzureChatOpenAI(
            api_key = AZURE_OPENAI_API_KEY,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
            azure_deployment = MODEL_NAME,
            api_version = "2025-01-01-preview",
            temperature = 0.5
        )

        self.retiever = retriever
        self.prompt   = get_prompt()
        self.qa_chain = self._create_chain()

    def _create_chain(self):
        combine_docs_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt = self.prompt
        )

        retrieval_chain = create_retrieval_chain(
            retriever=self.retiever,
            combine_docs_chain=combine_docs_chain
        )
        return retrieval_chain

    def get_recommendation(self, query:str):
        result = self.qa_chain.invoke({"input":query})
        return result.get('answer', result.get("result","No recommendation found"))


        
