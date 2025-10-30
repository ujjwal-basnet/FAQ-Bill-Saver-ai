# FAQ-Bill-Saver-ai

FAQ-Bill-Saver-ai is a small local prototype that caches AI responses (semantic + exact) for AWS SageMaker–related questions. It uses ChromaDB for persistent vector storage, SentenceTransformers for embeddings, and a Google Gemini based LLM connector for on-demand answers.

Features
- Exact-cache lookup using normalized query hashes.
- Semantic similarity search via vector embeddings.
- Falls back to LLM when cache miss occurs and stores results for future reuse.
- NLTK-based query normalization (lemmatization + POS-aware).

Prerequisites
- Linux environment (development and testing assumed on Linux).
- Python 3.10+ recommended.
- A Google Gemini API key (GEMINAI_API_KEY) for the LLM connector.
- Optional: Hugging Face credentials if using HF-hosted embedding models.

Install
1. Create and activate a virtual environment:
   sudo apt update
   sudo apt install -y python3-venv
   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

3. NLTK data (required for normalization):
   python -m nltk.downloader punkt averaged_perceptron_tagger wordnet

Environment variables
Create a `.env` file in the project root with at least:
- GEMINAI_API_KEY=<your_geminai_api_key>
- NOMIC_KEY=<optional>
- TAVILY_KEY=<optional>
- HUGGING_FACE=<optional>

Config
- Edit config.py / .env to change:
  - CHROMA_PERSIST_DIR (default: ./chroma_db)
  - COLLECTION_NAME (default: semantic_cache)
  - EMBEDDING_MODEL_NAME (default: BAAI/bge-base-en-v1.5)
  - GEMINAI_DEFULT_MODEL_NAME

Usage examples
- Quick test of the ask function:
  python ask_ai.py

- Simple programmatic usage (example):
  from config import settings
  from cache import Semantic_Cache, APPConfig

  # ensure settings are loaded or provide APPConfig with values
  sc = Semantic_Cache(config=settings)
  answer = sc.cache_check("what is aws sagemaker?")
  print(answer)

Notes and recommendations
- Add pydantic to requirements (already included in suggested requirements).
- Pin package versions for reproducibility.
- Clean up duplicate entries in requirements.txt.
- Ensure correct model names and API keys exist in .env before running.
- Consider handling errors from external services more explicitly (current code raises raw strings in some places).

Testing
- Run unit tests with pytest:
  pytest

Contributing
- Fork the repo, create a feature branch, add tests, and open a PR.

License
- Add an explicit license file if this project is to be shared publicly.
