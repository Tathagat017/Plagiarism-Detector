"""
Similarity service for calculating cosine similarity between embeddings.
"""

import logging
from typing import List, Tuple
import numpy as np
from scipy.spatial.distance import cosine

# Configure logging
logger = logging.getLogger(__name__)

class SimilarityService:
    """Service for calculating similarity between embeddings."""
    
    @staticmethod
    def calculate_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
        """
        Calculate pairwise cosine similarity matrix for embeddings.
        
        Args:
            embeddings: numpy array of embeddings with shape (n_texts, embedding_dim)
            
        Returns:
            numpy array similarity matrix with shape (n_texts, n_texts)
        """
        if embeddings.size == 0:
            raise ValueError("Empty embeddings array provided")
        
        n_texts = embeddings.shape[0]
        similarity_matrix = np.zeros((n_texts, n_texts))
        
        logger.info(f"Calculating similarity matrix for {n_texts} texts")
        
        # Calculate pairwise similarities
        for i in range(n_texts):
            for j in range(n_texts):
                if i == j:
                    # Diagonal elements are 1.0 (perfect similarity with self)
                    similarity_matrix[i, j] = 1.0
                elif i < j:
                    # Calculate cosine similarity
                    # Since embeddings are normalized, dot product = cosine similarity
                    similarity = np.dot(embeddings[i], embeddings[j])
                    similarity_matrix[i, j] = similarity
                    similarity_matrix[j, i] = similarity  # Matrix is symmetric
        
        logger.info("Similarity matrix calculation completed")
        return similarity_matrix
    
    @staticmethod
    def calculate_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        # Using scipy's cosine distance: cosine_similarity = 1 - cosine_distance
        return 1.0 - cosine(vec1, vec2)
    
    @staticmethod
    def find_similar_pairs(
        similarity_matrix: np.ndarray, 
        threshold: float = 0.7
    ) -> List[Tuple[int, int, float]]:
        """
        Find pairs of texts that exceed the similarity threshold.
        
        Args:
            similarity_matrix: NxN similarity matrix
            threshold: Similarity threshold (0.0 to 1.0)
            
        Returns:
            List of tuples (index1, index2, similarity_score) for similar pairs
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        
        similar_pairs = []
        n_texts = similarity_matrix.shape[0]
        
        # Only check upper triangle to avoid duplicates
        for i in range(n_texts):
            for j in range(i + 1, n_texts):
                similarity = similarity_matrix[i, j]
                if similarity >= threshold:
                    similar_pairs.append((i, j, similarity))
        
        # Sort by similarity score (descending)
        similar_pairs.sort(key=lambda x: x[2], reverse=True)
        
        logger.info(f"Found {len(similar_pairs)} similar pairs above threshold {threshold}")
        return similar_pairs
    
    @staticmethod
    def get_similarity_statistics(similarity_matrix: np.ndarray) -> dict:
        """
        Get statistics about the similarity matrix.
        
        Args:
            similarity_matrix: NxN similarity matrix
            
        Returns:
            Dictionary with statistics
        """
        n_texts = similarity_matrix.shape[0]
        
        # Get upper triangle (excluding diagonal)
        upper_triangle = []
        for i in range(n_texts):
            for j in range(i + 1, n_texts):
                upper_triangle.append(similarity_matrix[i, j])
        
        if not upper_triangle:
            return {
                "total_pairs": 0,
                "mean_similarity": 0.0,
                "max_similarity": 0.0,
                "min_similarity": 0.0,
                "std_similarity": 0.0
            }
        
        upper_triangle = np.array(upper_triangle)
        
        return {
            "total_pairs": len(upper_triangle),
            "mean_similarity": float(np.mean(upper_triangle)),
            "max_similarity": float(np.max(upper_triangle)),
            "min_similarity": float(np.min(upper_triangle)),
            "std_similarity": float(np.std(upper_triangle))
        }

# Create global instance
similarity_service = SimilarityService() 