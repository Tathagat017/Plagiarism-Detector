# Plagiarism Detector - Semantic Similarity Analyzer

A full-stack application for detecting potential plagiarism using semantic text similarity based on sentence embeddings. Built with **FastAPI** backend and **React** frontend.
![image](https://github.com/user-attachments/assets/516761f9-da13-4fd9-9b6d-5d7e778a3cb2)

![image](https://github.com/user-attachments/assets/11f16247-6592-4d27-8bc8-ad894b842b5c)



## 🚀 Features

- **Semantic Analysis**: Uses advanced sentence embedding models for accurate similarity detection
- **Multiple Models**: Support for 3 different embedding models (miniLM, mpnet, jina-small)
- **Configurable Thresholds**: Adjustable similarity thresholds for plagiarism detection
- **Interactive UI**: Modern React frontend with real-time analysis
- **Comprehensive Results**: Similarity matrix, plagiarism pairs, and detailed statistics
- **RESTful API**: Well-documented FastAPI backend with automatic OpenAPI documentation

## 🏗️ Architecture

```
plagiarism-detector/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API client
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
└── README.md              # This file
```

## 🧠 Embedding Models

| Model          | Description                   | Dimensions | Use Case                   |
| -------------- | ----------------------------- | ---------- | -------------------------- |
| **miniLM**     | `all-MiniLM-L6-v2`            | 384        | Fast, lightweight analysis |
| **mpnet**      | `all-mpnet-base-v2`           | 768        | Balanced performance       |
| **jina-small** | `jina-embeddings-v2-small-en` | 512        | Latest 2025 model          |

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 16+** (for frontend)
- **Git** (for cloning)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd plagiarism-detector
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python -m app.main
```

The backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Key Endpoints

| Method | Endpoint                   | Description                                |
| ------ | -------------------------- | ------------------------------------------ |
| `POST` | `/api/v1/analyze`          | Analyze texts for plagiarism               |
| `GET`  | `/api/v1/models`           | Get available embedding models             |
| `GET`  | `/api/v1/health`           | Health check                               |
| `POST` | `/api/v1/analyze/detailed` | Detailed analysis with multiple thresholds |
| `POST` | `/api/v1/compare`          | Compare two specific texts                 |

## 🎯 Usage

### 1. Web Interface

1. Open the frontend at `http://localhost:5173`
2. Configure your analysis settings:
   - Select an embedding model
   - Set similarity threshold (0.0 - 1.0)
3. Add text inputs (minimum 2, maximum 10)
4. Click "Analyze Plagiarism"
5. View results:
   - Similarity matrix with color-coded scores
   - Potential plagiarism pairs
   - Analysis statistics

### 2. API Usage

```bash
# Example: Analyze texts for plagiarism
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "The quick brown fox jumps over the lazy dog.",
      "A fast brown fox leaps over a sleepy dog.",
      "Python is a programming language."
    ],
    "model_key": "miniLM",
    "threshold": 0.7
  }'
```

## 🔧 Configuration

### Backend Configuration

Create a `.env` file in the backend directory:

```env
# Server Configuration
HOST=localhost
PORT=8000
DEBUG=true

# Model Configuration
DEFAULT_MODEL=miniLM
SIMILARITY_THRESHOLD=0.7

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### Frontend Configuration

The frontend API base URL can be configured in `frontend/src/services/api.ts`:

```typescript
const API_BASE_URL = "http://localhost:8000/api/v1";
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📦 Production Deployment

### Backend (Docker)

```bash
cd backend
docker build -t plagiarism-detector-backend .
docker run -p 8000:8000 plagiarism-detector-backend
```

### Frontend (Build)

```bash
cd frontend
npm run build
# Serve the dist/ directory with your web server
```

## 🛠️ Development

### Backend Development

```bash
cd backend
# Install development dependencies
pip install -r requirements-dev.txt

# Run with auto-reload
python -m app.main --reload

# Run tests
python -m pytest

# Format code
black app/
isort app/
```

### Frontend Development

```bash
cd frontend
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Requirements

### Backend Requirements

- Python 3.10+
- FastAPI
- Sentence Transformers
- PyTorch/TensorFlow
- Pydantic
- Uvicorn

### Frontend Requirements

- Node.js 16+
- React 18
- TypeScript
- Vite
- Mantine UI
- Axios

## 🔍 How It Works

1. **Text Input**: Users provide multiple text snippets for analysis
2. **Embedding Generation**: Selected model converts texts to high-dimensional vectors
3. **Similarity Calculation**: Cosine similarity computed between all text pairs
4. **Threshold Filtering**: Pairs above similarity threshold flagged as potential plagiarism
5. **Results Display**: Visual matrix and detailed reports presented to user

## 🎨 Screenshots

### Main Interface

- Sidebar with configuration options
- Multiple text input areas
- Model selection and threshold settings

### Results Display

- Color-coded similarity matrix
- Detailed plagiarism pairs with previews
- Analysis statistics and performance metrics

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**: Check Python version and virtual environment
2. **Frontend connection errors**: Ensure backend is running on port 8000
3. **Model loading errors**: Check internet connection for model downloads
4. **Memory issues**: Reduce batch size or use smaller models

### Debug Mode

Enable debug mode in backend `.env`:

```env
DEBUG=true
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) for embedding models
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) and [Mantine](https://mantine.dev/) for the frontend
- [Hugging Face](https://huggingface.co/) for model hosting

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for academic integrity and content originality**
