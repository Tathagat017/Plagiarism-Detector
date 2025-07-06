# Plagiarism Detector Backend

A FastAPI-based backend service for detecting plagiarism using semantic text similarity with sentence embeddings.

## Features

- 🔍 **Semantic Similarity Analysis**: Uses state-of-the-art sentence embedding models
- 🤖 **Multiple Models**: Supports 3 different embedding models for comparison
- 📊 **Similarity Matrix**: Generates complete pairwise similarity matrices
- 🎯 **Threshold Detection**: Configurable similarity thresholds for plagiarism detection
- 🚀 **Fast API**: RESTful API with automatic documentation
- 📝 **Detailed Results**: Provides text previews and similarity scores

## Supported Models

1. **all-MiniLM-L6-v2** (`miniLM`) - Lightweight, fast inference
2. **all-mpnet-base-v2** (`mpnet`) - High-quality embeddings, balanced performance
3. **jina-embeddings-v2-small-en** (`jina-small`) - Optimized for semantic search

## Installation

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Setup

1. **Clone the repository** (if not already done)
2. **Navigate to backend directory**

   ```bash
   cd backend
   ```

3. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On macOS/Linux
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration**
   - All configuration is hardcoded in `app/config.py`
   - No environment variables needed

## Usage

### Starting the Server

```bash
# Development mode (with auto-reload)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python app/main.py
```

The API will be available at:

- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Analyze Plagiarism

```http
POST /api/v1/analyze
Content-Type: application/json

{
  "texts": [
    "This is the first text to analyze.",
    "This is the second text to analyze.",
    "This is a completely different text."
  ],
  "model_key": "miniLM",
  "threshold": 0.7
}
```

#### 2. Get Available Models

```http
GET /api/v1/models
```

#### 3. Health Check

```http
GET /api/v1/health
```

#### 4. Detailed Analysis

```http
POST /api/v1/analyze/detailed
```

#### 5. Compare Two Texts

```http
POST /api/v1/compare
Content-Type: application/json

{
  "text1": "First text to compare",
  "text2": "Second text to compare",
  "model_key": "miniLM"
}
```

### Example Response

```json
{
  "similarity_matrix": [
    [1.0, 0.85, 0.23],
    [0.85, 1.0, 0.31],
    [0.23, 0.31, 1.0]
  ],
  "plagiarized_pairs": [
    {
      "index_1": 0,
      "index_2": 1,
      "similarity": 0.85,
      "text_1_preview": "This is the first text to analyze.",
      "text_2_preview": "This is the second text to analyze."
    }
  ],
  "model_used": "miniLM",
  "threshold_used": 0.7,
  "total_comparisons": 3,
  "execution_time": 1.23
}
```

## Configuration

### Hardcoded Settings

All configuration is defined in `app/config.py`:

```python
# Server Configuration
DEBUG = True
HOST = "0.0.0.0"
PORT = 8000

# Model Configuration
DEFAULT_MODEL = "miniLM"
SIMILARITY_THRESHOLD = 0.7

# Available Models
MODELS = {
    "miniLM": "all-MiniLM-L6-v2",
    "mpnet": "all-mpnet-base-v2",
    "jina-small": "jina-embeddings-v2-small-en"
}

# CORS Origins
CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Model Parameters

- **miniLM**: Fast, lightweight (384 dimensions)
- **mpnet**: Balanced performance (768 dimensions)
- **jina-small**: Optimized for search (512 dimensions)

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── api/
│   │   └── analyze.py       # API endpoints
│   ├── services/
│   │   ├── embeddings.py    # Embedding generation
│   │   ├── similarity.py    # Similarity calculations
│   │   └── detection.py     # Plagiarism detection logic
│   ├── models/
│   │   └── schema.py        # Pydantic models
│   └── utils/
│       └── preprocessing.py # Text preprocessing utilities
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

### Running Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Adding New Models

1. Update `MODELS` dictionary in `app/config.py`
2. Add model info to `EmbeddingService._model_info`
3. Update validation in `schema.py`

### Logging

The application uses Python's built-in logging. Logs include:

- Request/response information
- Model loading status
- Analysis execution times
- Error details

## Performance Considerations

- **Model Loading**: Models are loaded lazily on first use
- **Memory Usage**: Models stay in memory once loaded
- **Batch Processing**: Optimized for multiple texts
- **Caching**: Consider implementing Redis for production

## Troubleshooting

### Common Issues

1. **Model Download Fails**

   - Check internet connection
   - Verify model names in configuration
   - Check available disk space

2. **Out of Memory**

   - Reduce batch size
   - Use smaller models (miniLM)
   - Increase system memory

3. **Slow Performance**
   - Use GPU if available
   - Optimize batch sizes
   - Consider model size vs. accuracy trade-offs

### Debug Mode

Debug mode is enabled by default in `app/config.py`:

```python
DEBUG = True
```

This provides:

- Detailed error messages
- Request/response logging
- Auto-reload on code changes

## API Documentation

Visit `/docs` when the server is running for interactive API documentation with:

- Request/response schemas
- Example requests
- Try-it-out functionality
- Model descriptions

## License

This project is part of the MISOGI AI Assignment.
