"""
Detection service for plagiarism and clone detection logic.
"""

import logging
import time
from typing import List, Tuple
import numpy as np
from app.services.embeddings import embedding_service
from app.services.similarity import similarity_service
from app.models.schema import SimilarityPair

# Configure logging
logger = logging.getLogger(__name__)

class DetectionService:
    """Service for plagiarism and clone detection."""
    
    def __init__(self):
        """Initialize the detection service."""
        self.embedding_service = embedding_service
        self.similarity_service = similarity_service
    
    def analyze_texts(
        self, 
        texts: List[str], 
        model_key: str = "miniLM", 
        threshold: float = 0.7
    ) -> Tuple[np.ndarray, List[SimilarityPair], dict]:
        """
        Perform complete plagiarism analysis on texts.
        
        Args:
            texts: List of text strings to analyze
            model_key: Model key to use for embeddings
            threshold: Similarity threshold for clone detection
            
        Returns:
            Tuple of (similarity_matrix, plagiarized_pairs, metadata)
        """
        start_time = time.time()
        
        logger.info(f"Starting plagiarism analysis for {len(texts)} texts")
        logger.info(f"Using model: {model_key}, threshold: {threshold}")
        
        # Step 1: Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(texts, model_key)
        
        # Step 2: Calculate similarity matrix
        similarity_matrix = self.similarity_service.calculate_similarity_matrix(embeddings)
        
        # Step 3: Find similar pairs
        similar_pairs_raw = self.similarity_service.find_similar_pairs(
            similarity_matrix, threshold
        )
        
        # Step 4: Create detailed similarity pairs
        plagiarized_pairs = self._create_similarity_pairs(
            similar_pairs_raw, texts
        )
        
        # Step 5: Calculate metadata
        execution_time = time.time() - start_time
        total_comparisons = len(texts) * (len(texts) - 1) // 2
        
        metadata = {
            "model_used": model_key,
            "threshold_used": threshold,
            "total_comparisons": total_comparisons,
            "execution_time": execution_time,
            "similarity_stats": self.similarity_service.get_similarity_statistics(similarity_matrix)
        }
        
        logger.info(f"Analysis completed in {execution_time:.2f} seconds")
        logger.info(f"Found {len(plagiarized_pairs)} plagiarized pairs")
        
        return similarity_matrix, plagiarized_pairs, metadata
    
    def _create_similarity_pairs(
        self, 
        similar_pairs_raw: List[Tuple[int, int, float]], 
        texts: List[str]
    ) -> List[SimilarityPair]:
        """
        Create detailed similarity pairs from raw similarity data.
        
        Args:
            similar_pairs_raw: List of (index1, index2, similarity) tuples
            texts: Original texts
            
        Returns:
            List of SimilarityPair objects
        """
        similarity_pairs = []
        
        for index1, index2, similarity in similar_pairs_raw:
            # Create text previews (first 100 characters)
            text1_preview = self._create_text_preview(texts[index1])
            text2_preview = self._create_text_preview(texts[index2])
            
            similarity_pair = SimilarityPair(
                index_1=index1,
                index_2=index2,
                similarity=float(similarity),
                text_1_preview=text1_preview,
                text_2_preview=text2_preview
            )
            
            similarity_pairs.append(similarity_pair)
        
        return similarity_pairs
    
    def _create_text_preview(self, text: str, max_length: int = 100) -> str:
        """
        Create a preview of text for display.
        
        Args:
            text: Full text string
            max_length: Maximum length of preview
            
        Returns:
            Text preview with ellipsis if truncated
        """
        text = text.strip()
        if len(text) <= max_length:
            return text
        
        # Truncate and add ellipsis
        truncated = text[:max_length].rstrip()
        
        # Try to break at word boundary
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # If space is reasonably close to end
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    def detect_potential_plagiarism(
        self, 
        texts: List[str], 
        model_key: str = "miniLM",
        strict_threshold: float = 0.85,
        moderate_threshold: float = 0.7
    ) -> dict:
        """
        Detect potential plagiarism with multiple severity levels.
        
        Args:
            texts: List of text strings to analyze
            model_key: Model key to use for embeddings
            strict_threshold: Threshold for high-confidence plagiarism
            moderate_threshold: Threshold for moderate-confidence plagiarism
            
        Returns:
            Dictionary with plagiarism analysis results
        """
        similarity_matrix, _, metadata = self.analyze_texts(texts, model_key, moderate_threshold)
        
        # Find pairs at different thresholds
        strict_pairs = self.similarity_service.find_similar_pairs(
            similarity_matrix, strict_threshold
        )
        moderate_pairs = self.similarity_service.find_similar_pairs(
            similarity_matrix, moderate_threshold
        )
        
        # Create detailed pairs
        strict_similarity_pairs = self._create_similarity_pairs(strict_pairs, texts)
        moderate_similarity_pairs = self._create_similarity_pairs(moderate_pairs, texts)
        
        return {
            "high_confidence_plagiarism": strict_similarity_pairs,
            "moderate_confidence_plagiarism": moderate_similarity_pairs,
            "similarity_matrix": similarity_matrix.tolist(),
            "metadata": metadata
        }
    
    def get_text_similarity_report(
        self, 
        text1: str, 
        text2: str, 
        model_key: str = "miniLM"
    ) -> dict:
        """
        Get detailed similarity report for two specific texts.
        
        Args:
            text1: First text
            text2: Second text
            model_key: Model key to use for embeddings
            
        Returns:
            Dictionary with detailed similarity report
        """
        texts = [text1, text2]
        similarity_matrix, _, metadata = self.analyze_texts(texts, model_key, 0.0)
        
        similarity_score = similarity_matrix[0, 1]
        
        return {
            "similarity_score": float(similarity_score),
            "is_highly_similar": similarity_score >= 0.85,
            "is_moderately_similar": similarity_score >= 0.7,
            "text1_preview": self._create_text_preview(text1),
            "text2_preview": self._create_text_preview(text2),
            "model_used": model_key,
            "analysis_time": metadata["execution_time"]
        }

# Create global instance
detection_service = DetectionService() 