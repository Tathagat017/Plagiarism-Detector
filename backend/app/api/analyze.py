"""
API routes for plagiarism analysis endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.models.schema import (
    AnalyzeRequest, 
    AnalyzeResponse, 
    ModelsResponse, 
    HealthResponse
)
from app.services.detection import detection_service
from app.services.embeddings import embedding_service
from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_plagiarism(request: AnalyzeRequest):
    """
    Analyze texts for plagiarism using semantic similarity.
    
    Args:
        request: AnalyzeRequest containing texts, model_key, and threshold
        
    Returns:
        AnalyzeResponse with similarity matrix and plagiarized pairs
    """
    try:
        logger.info(f"Received analysis request for {len(request.texts)} texts")
        logger.info(f"Model: {request.model_key}, Threshold: {request.threshold}")
        
        # Perform plagiarism analysis
        similarity_matrix, plagiarized_pairs, metadata = detection_service.analyze_texts(
            texts=request.texts,
            model_key=request.model_key,
            threshold=request.threshold
        )
        
        # Convert similarity matrix to list of lists for JSON serialization
        similarity_matrix_list = similarity_matrix.tolist()
        
        # Create response
        response = AnalyzeResponse(
            similarity_matrix=similarity_matrix_list,
            plagiarized_pairs=plagiarized_pairs,
            model_used=metadata["model_used"],
            threshold_used=metadata["threshold_used"],
            total_comparisons=metadata["total_comparisons"],
            execution_time=metadata["execution_time"]
        )
        
        logger.info(f"Analysis completed successfully in {metadata['execution_time']:.2f}s")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis"
        )

@router.get("/models", response_model=ModelsResponse)
async def get_available_models():
    """
    Get information about available embedding models.
    
    Returns:
        ModelsResponse with available models and descriptions
    """
    try:
        model_info = embedding_service.get_all_model_info()
        
        response = ModelsResponse(
            available_models=settings.get_available_models(),
            default_model=settings.DEFAULT_MODEL,
            model_descriptions={
                key: {
                    "name": info["name"],
                    "description": info["description"],
                    "dimensions": info["dimensions"],
                    "loaded": embedding_service.is_model_loaded(key)
                }
                for key, info in model_info.items()
            }
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve model information"
        )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse with system status
    """
    try:
        # Check if at least one model can be loaded
        models_loaded = False
        try:
            # Try to load the default model
            embedding_service._load_model(settings.DEFAULT_MODEL)
            models_loaded = True
        except Exception:
            models_loaded = False
        
        response = HealthResponse(
            status="healthy",
            version="1.0.0",
            models_loaded=models_loaded
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Health check failed"
        )

@router.post("/analyze/detailed")
async def analyze_plagiarism_detailed(request: AnalyzeRequest):
    """
    Analyze texts for plagiarism with detailed multi-level results.
    
    Args:
        request: AnalyzeRequest containing texts, model_key, and threshold
        
    Returns:
        Detailed plagiarism analysis with multiple confidence levels
    """
    try:
        logger.info(f"Received detailed analysis request for {len(request.texts)} texts")
        
        # Perform detailed plagiarism analysis
        result = detection_service.detect_potential_plagiarism(
            texts=request.texts,
            model_key=request.model_key,
            strict_threshold=0.85,
            moderate_threshold=request.threshold
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during detailed analysis"
        )

@router.post("/compare")
async def compare_two_texts(
    text1: str,
    text2: str,
    model_key: str = "miniLM"
):
    """
    Compare two specific texts for similarity.
    
    Args:
        text1: First text to compare
        text2: Second text to compare
        model_key: Model key to use for embeddings
        
    Returns:
        Detailed similarity report for the two texts
    """
    try:
        if not text1.strip() or not text2.strip():
            raise ValueError("Both texts must be non-empty")
        
        logger.info("Received request to compare two texts")
        
        # Get detailed similarity report
        result = detection_service.get_text_similarity_report(
            text1=text1,
            text2=text2,
            model_key=model_key
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during text comparison"
        ) 