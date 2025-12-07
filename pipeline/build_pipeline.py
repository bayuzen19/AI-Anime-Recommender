from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.custom_exeception import CustomException
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting Load Documents...")
        loader  = AnimeDataLoader("./data/anime_with_synopsis.csv","./data/anime_updated.csv")
        processed_csv = loader.load_and_process()
        logger.info('Data loaded and processed')

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.builder_and_save_vectorstore()
        logger.info("Vector store built successfully...")
    except Exception as e:
        logger.error(f"Failed to process or built vector store {str(e)} ")
        raise CustomException('Failed to process or build vector store',e)

if __name__ == "__main__":
    main()