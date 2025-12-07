from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

class VectorStoreBuilder:
    def __init__(self,csv_path:str, persist_dir:str="chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embeddings  = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def builder_and_save_vectorstore(self):
        loader_csv = CSVLoader(file_path = self.csv_path,
                               encoding="utf-8",
                               metadata_columns=[]
                               )
        data     = loader_csv.load()
        splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=int(0.15*1024))
        texts    = splitter.split_documents(data)

        db       = Chroma.from_documents(documents=texts, 
                                         embedding=self.embeddings,
                                         persist_directory=self.persist_dir
                                         )
        db.persist()

    def load_vector_store(self):
        return Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
    