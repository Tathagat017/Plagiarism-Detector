**Product Requirements Document (PRD)**

---

## Project Title:

**Plagiarism Detector - Semantic Similarity Analyzer**

## Objective:

Build a full-stack MVP application with a **FastAPI backend** and **React frontend** to detect potential plagiarism using **semantic text similarity** based on sentence embeddings.

---

## Core Features:

1. Input multiple text snippets via a web interface
2. Generate sentence embeddings using open-source models
3. Compute pairwise cosine similarity between text inputs
4. Identify highly similar (potentially plagiarized) pairs
5. Visualize results as a similarity matrix
6. Support multiple embedding models for comparison

---

## Embedding Models Used:

- `all-MiniLM-L6-v2` (Sentence-Transformers)
- `all-mpnet-base-v2` (Sentence-Transformers)
- `jina-embeddings-v2-small-en` (Jina AI, 2025 release)

---

## Backend Technology:

- **Framework:** FastAPI
- **Language:** Python 3.10+
- **Key Libraries:**
  - `fastapi`, `uvicorn`
  - `pydantic`, `python-dotenv`
  - `sentence-transformers`, `transformers`, `torch`
  - `scipy`, `numpy`
  - `httpx`, `pytest`

---

## Project Structure:

```
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── api/
│   │   └── analyze.py          # API route for similarity analysis
│   ├── services/
│   │   ├── embeddings.py       # Embedding generation logic
│   │   ├── similarity.py       # Cosine similarity calculation
│   │   ├── detection.py        # Clone detection logic
│   ├── models/
│   │   └── schema.py           # Pydantic request/response models
│   ├── config.py               # Environment configuration
│   └── utils/
│       └── preprocessing.py    # Optional text normalization
├── .env
├── requirements.txt
└── README.md
```

---

## PHASED BACKEND IMPLEMENTATION PLAN

### 🔹 PHASE 1: Design & Setup

- Create folder structure and initialize FastAPI
- Install dependencies
- Add .env and config loading for model names, thresholds, etc.

### 🔹 PHASE 2: Input Handling & API Interface

- Define `AnalyzeRequest` and `AnalyzeResponse` in `models/schema.py`
- Include fields: `texts`, `model_key`, `threshold`

### 🔹 PHASE 3: Embedding Generation Module

- Implement `generate_embeddings(texts: List[str], model_key: str)`
- Handle the three model keys: `miniLM`, `mpnet`, `jina-small`
- Use `SentenceTransformer(..., trust_remote_code=True)`
- Apply lazy loading or singleton pattern

### 🔹 PHASE 4: Pairwise Similarity Computation

- Implement `calculate_similarity(embeddings: List[np.ndarray])`
- Compute cosine similarity matrix (NxN)
- Ensure symmetric and diagonal = 1.0

### 🔹 PHASE 5: Clone Detection

- Implement `detect_clones(matrix: List[List[float]], threshold: float)`
- Return all (i, j) pairs where `similarity >= threshold`

### 🔹 PHASE 6: API Endpoint

- Define `POST /analyze` endpoint
- Use async FastAPI route
- Return:
  - 2D similarity matrix
  - List of plagiarized pairs (with indices and similarity)

### 🔹 PHASE 7: CORS & Env Configuration

- Add CORS middleware for frontend connection
- Load Open Source model paths via `.env` or `config.py`

### 🔹 PHASE 8: Testing & Validation

- Create unit tests for:
  - Embedding generation
  - Similarity calculation
  - Threshold filtering
  - Endpoint response
- Use `pytest` + `FastAPI TestClient`

### 🔹 PHASE 9: Optional Enhancements

- Add `/models` endpoint for model listing
- Add export options (CSV, JSON)
- Log execution times for benchmarking
- Introduce async background task handling for large batches

---

## Deliverables:

- FastAPI backend that:
  - Accepts multiple input texts
  - Supports 3 open-source embedding models
  - Returns similarity matrix + detected clones
- Fully documented API and modules
- Test coverage for core logic

---

## Future Considerations:

- Add support for multilingual embeddings
- User-based session handling and saving results
- Visual analytics dashboard
- Scale with GPU for real-time performance

---

## Frontend

Single page application with a sidebar and a main content area.

- **Framework:** React
- **Language:** TypeScript
- **Key Libraries:**
  - React 18
  - Mantine UI
  - axios
  - React fontawesome icons
