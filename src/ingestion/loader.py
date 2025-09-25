from langchain.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.embeddings.jina_embeddings import JinaEmbeddings
from langchain.vectorstores import PGVector
from config import Config

def load_and_embed_documents():
    loader = DirectoryLoader(
        path="data/hr_policies",
        glob="**/*.md",
        loader_cls=UnstructuredMarkdownLoader,
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    embeddings = JinaEmbeddings(model_name=Config.EMBEDDING_MODEL)

    db = PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=Config.COLLECTION_NAME,
        connection_string=Config.DATABASE_URL,
        use_jsonb=True,
    )
    return db