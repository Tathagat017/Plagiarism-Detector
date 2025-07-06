# Plagiarism Detector Frontend

A modern React frontend for the Plagiarism Detector API, built with Vite, TypeScript, and Mantine UI.

## Features

- **Modern UI**: Clean, responsive design with Mantine UI components
- **Multiple Text Input**: Support for analyzing multiple text snippets (up to 10)
- **Model Selection**: Choose from different embedding models (miniLM, mpnet, jina-small)
- **Configurable Threshold**: Adjust similarity threshold for plagiarism detection
- **Visual Results**:
  - Similarity matrix with color-coded similarity scores
  - Detailed plagiarism pairs with text previews
  - Analysis statistics and execution metrics
- **Real-time Feedback**: Loading states, error handling, and success notifications

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Mantine UI** - Component library
- **Axios** - HTTP client
- **FontAwesome** - Icons

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Integration

The frontend communicates with the FastAPI backend through the following endpoints:

- `GET /api/v1/models` - Get available embedding models
- `POST /api/v1/analyze` - Analyze texts for plagiarism
- `GET /api/v1/health` - Health check

## Usage

1. **Configure Settings**: Select an embedding model and set the similarity threshold
2. **Add Text Inputs**: Enter at least 2 texts to analyze
3. **Run Analysis**: Click "Analyze Plagiarism" to start the semantic similarity analysis
4. **View Results**:
   - Check the similarity matrix for all pairwise comparisons
   - Review potential plagiarism cases above the threshold
   - View analysis statistics and performance metrics

## Configuration

The API base URL can be modified in `src/services/api.ts`:

```typescript
const API_BASE_URL = "http://localhost:8000/api/v1";
```

## Development

### Project Structure

```
src/
├── components/          # Reusable UI components (future)
├── services/           # API service layer
├── types/             # TypeScript type definitions
├── App.tsx            # Main application component
└── main.tsx           # Application entry point
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
