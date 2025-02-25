# rag-test
  
## Introduction:  
- A test repo for learning RAG model  
- Allows you to query a set of documents using Chatbot  
- Tech stack:  
  + LLaMa3.2:3b as LLM  
  + BAAI/bge-small-en-v1.5 as embedding model  
  + ChromaDB as a vector database for the documents  
  + Streamlit for interface  
  
## Structure of the Repo:  
<pre>
rag-test/  
│  
├── chroma/                  # Vector database of the documents (for faster queries)  
├── modules/                 # Folders with modules  
│   ├── __init__.py          # File __init__ for module  
│   ├── ollama_utils/        # Utils for Ollama (class OllamaAPI, funct parse_multiple_json(), embed_model and llm_model)  
│   │   ├── __init__.py  
│   │   ├── ollama_api.py  
│   │   └── param.py         # Includes model's name  
│   └── streamlit_utils/     # Utils for streamlit (display_message(), launching(), avatars)  
│       ├── __init__.py  
│       ├── param.py  
│       └── utils.py  
├── .gitignore  
├── embed_utils.py  
├── requirements.txt  
└── README.md  
</pre>
