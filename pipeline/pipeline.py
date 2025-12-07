from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import *
from utils.logger import get_logger
from utils.custom_exeception import CustomException

logger = get_logger(__name__)

class AnimeRecommendetionPipeline:

    def __init__(self,persist_dir="chroma_db"):
        try:
            logger.info("Initialize Recommendation Pipeline")
            vector_builder = VectorStoreBuilder(csv_path="",persist_dir=persist_dir)
            retriever = vector_builder.load_vector_store().as_retriever()
            self.recommender = AnimeRecommender(retriever)
            logger.info("Pipeline intialized successfully...")
        except Exception as e:
            logger.error(f"Failed to build pipeline {str(e)}")
            raise CustomException("Error during build pipeline",e)
        
    def recommender(self,query:str) -> str:
        try:
            logger.info(f"Received a query {query}")
            recommendation = self.recommender.get_recommendation(query)
            logger.info("Recommendation generate successfully...")
            return recommendation
        except Exception as e:
            logger.error(f"Failed to generate recommendation {str(e)}")
            raise CustomException("Failed to generate recommendation",e)