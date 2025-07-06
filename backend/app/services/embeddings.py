"""
Embeddings service for generating sentence embeddings using various models.
"""

import logging
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating sentence embeddings."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self._models: Dict[str, SentenceTransformer] = {}
        self._model_info: Dict[str, Dict] = {
            "miniLM": {
                "name": "all-MiniLM-L6-v2",
                "description": "Lightweight model, fast inference, good for general use",
                "dimensions": 384
            },
            "mpnet": {
                "name": "all-mpnet-base-v2",
                "description": "High-quality embeddings, balanced speed and accuracy",
                "dimensions": 768
            },
            "jina-small": {
                "name": "jina-embeddings-v2-small-en",
                "description": "Jina AI model, optimized for semantic search",
                "dimensions": 512
            }
        }
    
    def _load_model(self, model_key: str) -> SentenceTransformer:
        """Load a model if not already loaded."""
        if model_key not in self._models:
            model_name = settings.get_model_name(model_key)
            logger.info(f"Loading model: {model_name} (key: {model_key})")
            
            try:
                # Load with trust_remote_code=True for Jina models
                trust_remote = model_key == "jina-small"
                self._models[model_key] = SentenceTransformer(
                    model_name, 
                    trust_remote_code=trust_remote
                )
                logger.info(f"Successfully loaded model: {model_key}")
            except Exception as e:
                logger.error(f"Failed to load model {model_key}: {str(e)}")
                raise RuntimeError(f"Failed to load model {model_key}: {str(e)}")
        
        return self._models[model_key]
    
    def generate_embeddings(self, texts: List[str], model_key: str = "miniLM") -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            model_key: Model key to use for embeddings
            
        Returns:
            numpy array of embeddings with shape (n_texts, embedding_dim)
        """
        if not texts:
            raise ValueError("No texts provided for embedding generation")
        
        # Validate model key
        if model_key not in settings.get_available_models():
            raise ValueError(f"Invalid model key: {model_key}")
        
        # Load model
        model = self._load_model(model_key)
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(texts)} texts using {model_key}")
        try:
            embeddings = model.encode(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,  # Normalize for cosine similarity
                show_progress_bar=len(texts) > 10
            )
            
            logger.info(f"Generated embeddings shape: {embeddings.shape}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")
    
    def get_model_info(self, model_key: str) -> Dict:
        """Get information about a specific model."""
        if model_key not in self._model_info:
            raise ValueError(f"Unknown model key: {model_key}")
        return self._model_info[model_key]
    
    def get_all_model_info(self) -> Dict[str, Dict]:
        """Get information about all available models."""
        return self._model_info
    
    def is_model_loaded(self, model_key: str) -> bool:
        """Check if a model is already loaded in memory."""
        return model_key in self._models
    
    def unload_model(self, model_key: str) -> None:
        """Unload a model from memory."""
        if model_key in self._models:
            del self._models[model_key]
            logger.info(f"Unloaded model: {model_key}")
    
    def clear_all_models(self) -> None:
        """Clear all loaded models from memory."""
        self._models.clear()
        logger.info("Cleared all models from memory")

# Create global instance
embedding_service = EmbeddingService() 