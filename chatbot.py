### IMPORT
# For web
import streamlit as st
from modules.streamlit_utils import launching, display_message, avatars
from torch import classes

# For RAG model
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
import chromadb
from modules.ollama_utils import embed_model, llm_model, model_name



### WEB INTERFACE
# Launching
launching()
classes.__path__ = [] # Must have to avoid error

# Welcoming message
if "opened" not in st.session_state:
    # Set opened to True
    st.session_state.opened = True

    # Display welcoming message
    welcome = "Hello user, this is your personal assistant! How may I help you?"
    display_message("assistant", avatars["assistant"], welcome)

# User input
question = st.chat_input(
    placeholder = "Can you give me a short summary?",
)



### CHATBOT
# Config
Settings.llm = Ollama(model = model_name, temperature = 0.75)

# Indexing and storing embedding to disk
client = chromadb.PersistentClient()
try:
    collection = client.create_collection(name = "docs")
except:
    collection = client.get_collection(name = "docs")

if question:
    # Display user's question
    display_message("user", avatars["user"], question)

    try:
        # Assign chroma as the vector_store to the context
        vector_store = ChromaVectorStore(chroma_collection = collection, persist_dir = "./chroma")

        # Load your index from stored vectors
        index = VectorStoreIndex.from_vector_store(vector_store, embed_model = embed_model)
        query_engine = index.as_query_engine(llm = llm_model, streaming = True)
        response = query_engine.query(question)
        response = str(response)

    except Exception as e:
        response = f"Error calling Ollama API: {str(e)}"

    # Display answer from Ollama
    display_message("assistant", avatars["assistant"], response)