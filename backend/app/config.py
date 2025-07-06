"""
Configuration module for the Plagiarism Detector backend.
Contains hardcoded application settings.
"""

from typing import List, Dict

class Settings:
    """Application settings with hardcoded values."""
    
    # Server Configuration
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model Configuration
    DEFAULT_MODEL: str = "miniLM"
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Available Models Mapping
    MODELS: Dict[str, str] = {
        "miniLM": "all-MiniLM-L6-v2",
        "mpnet": "all-mpnet-base-v2",
        "jina-small": "jina-embeddings-v2-small-en"
    }
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
    "*"
    ]
    
    @classmethod
    def get_model_name(cls, model_key: str) -> str:
        """Get the actual model name from the model key."""
        return cls.MODELS.get(model_key, cls.MODELS[cls.DEFAULT_MODEL])
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """Get list of available model keys."""
        return list(cls.MODELS.keys())

# Create settings instance
settings = Settings() 