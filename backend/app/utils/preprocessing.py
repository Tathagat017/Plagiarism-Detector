"""
Text preprocessing utilities for normalizing text before analysis.
"""

import re
import string
from typing import List, Optional

class TextPreprocessor:
    """Text preprocessing utilities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Basic text cleaning.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def normalize_text(text: str, remove_punctuation: bool = False) -> str:
        """
        Normalize text by converting to lowercase and optionally removing punctuation.
        
        Args:
            text: Input text string
            remove_punctuation: Whether to remove punctuation
            
        Returns:
            Normalized text string
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation if requested
        if remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Clean whitespace
        text = TextPreprocessor.clean_text(text)
        
        return text
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """
        Remove URLs from text.
        
        Args:
            text: Input text string
            
        Returns:
            Text with URLs removed
        """
        if not text:
            return ""
        
        # Remove URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        text = re.sub(url_pattern, '', text)
        
        # Clean whitespace
        text = TextPreprocessor.clean_text(text)
        
        return text
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """
        Remove email addresses from text.
        
        Args:
            text: Input text string
            
        Returns:
            Text with email addresses removed
        """
        if not text:
            return ""
        
        # Remove email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, '', text)
        
        # Clean whitespace
        text = TextPreprocessor.clean_text(text)
        
        return text
    
    @staticmethod
    def remove_special_characters(text: str, keep_spaces: bool = True) -> str:
        """
        Remove special characters from text.
        
        Args:
            text: Input text string
            keep_spaces: Whether to keep spaces
            
        Returns:
            Text with special characters removed
        """
        if not text:
            return ""
        
        if keep_spaces:
            # Keep only alphanumeric characters and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        else:
            # Keep only alphanumeric characters
            text = re.sub(r'[^a-zA-Z0-9]', '', text)
        
        # Clean whitespace
        text = TextPreprocessor.clean_text(text)
        
        return text
    
    @staticmethod
    def preprocess_for_similarity(
        text: str,
        remove_urls: bool = True,
        remove_emails: bool = True,
        normalize: bool = True,
        remove_punctuation: bool = False
    ) -> str:
        """
        Comprehensive preprocessing for similarity analysis.
        
        Args:
            text: Input text string
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove email addresses
            normalize: Whether to normalize (lowercase)
            remove_punctuation: Whether to remove punctuation
            
        Returns:
            Preprocessed text string
        """
        if not text:
            return ""
        
        # Start with basic cleaning
        processed_text = TextPreprocessor.clean_text(text)
        
        # Remove URLs if requested
        if remove_urls:
            processed_text = TextPreprocessor.remove_urls(processed_text)
        
        # Remove emails if requested
        if remove_emails:
            processed_text = TextPreprocessor.remove_emails(processed_text)
        
        # Normalize if requested
        if normalize:
            processed_text = TextPreprocessor.normalize_text(
                processed_text, 
                remove_punctuation=remove_punctuation
            )
        
        return processed_text
    
    @staticmethod
    def preprocess_texts(
        texts: List[str],
        remove_urls: bool = True,
        remove_emails: bool = True,
        normalize: bool = True,
        remove_punctuation: bool = False
    ) -> List[str]:
        """
        Preprocess a list of texts.
        
        Args:
            texts: List of input text strings
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove email addresses
            normalize: Whether to normalize (lowercase)
            remove_punctuation: Whether to remove punctuation
            
        Returns:
            List of preprocessed text strings
        """
        return [
            TextPreprocessor.preprocess_for_similarity(
                text,
                remove_urls=remove_urls,
                remove_emails=remove_emails,
                normalize=normalize,
                remove_punctuation=remove_punctuation
            )
            for text in texts
        ]
    
    @staticmethod
    def get_text_stats(text: str) -> dict:
        """
        Get statistics about a text.
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary with text statistics
        """
        if not text:
            return {
                "char_count": 0,
                "word_count": 0,
                "sentence_count": 0,
                "paragraph_count": 0
            }
        
        # Character count
        char_count = len(text)
        
        # Word count
        words = text.split()
        word_count = len(words)
        
        # Sentence count (approximate)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Paragraph count (approximate)
        paragraphs = text.split('\n\n')
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        return {
            "char_count": char_count,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count
        }

# Create global instance
text_preprocessor = TextPreprocessor() 