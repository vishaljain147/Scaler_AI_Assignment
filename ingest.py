from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# Load documents
documents = []

knowledge_path = "knowledge"

if not os.path.exists(knowledge_path):
    raise FileNotFoundError(
        f"Knowledge folder not found: {knowledge_path}"
    )

for file in os.listdir(knowledge_path):

    path = os.path.join(knowledge_path, file)

    try:
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

        elif file.endswith(".md"):
            loader = TextLoader(path, encoding="utf-8")
            documents.extend(loader.load())

    except Exception as e:
        print(f"Error loading {file}: {e}")

print(f"Loaded {len(documents)} document pages")

# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = splitter.split_documents(documents)

print(f"Created {len(docs)} chunks")

# Local embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector DB
vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("Knowledge Base Created Successfully!")
print("Vector database saved in: chroma_db")