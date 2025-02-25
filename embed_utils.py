from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, load_index_from_storage
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import chromadb
from modules.ollama_utils import embed_model, model_name
from llama_index.core import Settings

Settings.llm = Ollama(model = model_name, temperature = 0.75)

# Load document
"""

documents at first is a Document class of llama_index
by using get_content() we change it into string type

"""
documents = SimpleDirectoryReader(input_dir = "./static/document").load_data()
documents = [d.get_content() for d in documents]

# Indexing and storing embedding to disk
client = chromadb.PersistentClient()
try:
    collection = client.create_collection(name = "docs")
except:
    collection = client.get_collection(name = "docs")

for i, d in enumerate(documents): # store each document in a vector embedding database, d should be strings
    embeddings = embed_model.get_text_embedding(d)
    collection.add(
        ids=[str(i)],
        embeddings=embeddings,
        documents=[d]
    )

if __name__ == "__main__":
    # Assign chroma as the vector_store to the context
    vector_store = ChromaVectorStore(chroma_collection = collection, persist_dir = "./chroma")

    # Load your index from stored vectors
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model = embed_model)
    query_engine = index.as_query_engine(llm = None, streaming = True)
    response = query_engine.query("Bạn hãy kể về dàn ý thuyết trình của nhóm ta về Situational Leadership!")
    response.print_response_stream()