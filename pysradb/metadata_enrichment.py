"""
Metadata enrichment for SRA/GEO datasets using LLMs and embeddings.
"""

import logging
import os
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, Field
from tqdm.autonotebook import tqdm

logger = logging.getLogger(__name__)


def _prompt_install_enrichment_dependencies() -> bool:
    """
    Prompt user to install enrichment dependencies.

    Returns:
        True if installation succeeded, False otherwise.
    """
    pass


class MetadataExtractor(ABC):
    """Base class for metadata extraction from experiment descriptions."""

    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def extract_metadata(
        self, text: str, fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract metadata from text.

        Args:
            text: Input text (experiment description, title, etc.)
            fields: List of metadata fields to extract. If None, extract all.

        Returns:
            Dictionary with extracted metadata
        """
        pass

    def extract_batch(
        self, texts: List[str], fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Extract metadata from multiple texts.

        Args:
            texts: List of input texts
            fields: List of metadata fields to extract

        Returns:
            List of dictionaries with extracted metadata
        """
        raise NotImplementedError

    def _find_column_variant(self, df: pd.DataFrame, target_col: str) -> Optional[str]:
        """
        Find a column that matches the target column name with flexible matching.

        Handles variations like:
        - Different casing: cell_type, Cell_Type, CELL_TYPE
        - Spaces vs underscores: cell_type, cell type, celltype
        - CamelCase: cellType, CellType

        Args:
            df: DataFrame to search
            target_col: Target column name (e.g., 'cell_type')

        Returns:
            Actual column name if found, None otherwise
        """
        raise NotImplementedError

    def enrich_dataframe(
        self,
        df: pd.DataFrame,
        text_column: Optional[str] = None,
        fields: Optional[List[str]] = None,
        prefix: str = "guessed_",
        show_progress: bool = True,
    ) -> pd.DataFrame:
        """
        Enrich a DataFrame with extracted metadata.

        Args:
            df: Input DataFrame
            text_column: Column containing text to analyze. If None, combines sample text columns.
            fields: List of metadata fields to extract
            prefix: Prefix for new columns
            show_progress: Show progress bar (default: True)

        Returns:
            DataFrame with additional metadata columns
        """
        # If text_column not specified, combine all relevant columns
        raise NotImplementedError


class _MetadataExtraction(BaseModel):
    """Model for metadata extraction aligned with CellxGene schema.

    Fields are designed to match CellxGene Discover metadata structure and use
    ontology-based terms from UBERON (anatomy), MONDO (disease), and CL (cell types).

    Anatomical hierarchy: anatomical_system → organ → tissue
    """

    organ: str = Field(
        default="Unknown",
        description="High-level organ (e.g., brain, liver, heart, lung, breast)",
    )
    tissue: str = Field(
        default="Unknown", description="Specific tissue within organ (UBERON-based)"
    )
    anatomical_system: str = Field(
        default="Unknown",
        description="Body system (e.g., cardiovascular, nervous, immune)",
    )
    cell_type: str = Field(
        default="Unknown", description="Specific cell type (CL ontology-based)"
    )
    disease: str = Field(
        default="Unknown", description="Disease or condition (MONDO ontology-based)"
    )
    sex: str = Field(
        default="Unknown", description="Biological sex (male, female, mixed, Unknown)"
    )
    development_stage: str = Field(
        default="Unknown",
        description="Developmental stage (embryonic, fetal, adult, etc.)",
    )
    assay: str = Field(
        default="Unknown",
        description="Experimental assay type (RNA-seq, scRNA-seq, ATAC-seq, etc.)",
    )
    organism: str = Field(
        default="Unknown", description="Species (Homo sapiens, Mus musculus, etc.)"
    )


DEFAULT_LLM_PROVIDER = "ollama/phi3"


def load_ontology_reference() -> Dict[str, List[str]]:
    """
    Returns comprehensive reference categories from UBERON, MONDO, and CL ontologies.

    Returns:
        Dictionary with ontology terms (organs, tissues, anatomical_systems, cell_types, diseases)
    """
    pass


class LLMMetadataExtractor(MetadataExtractor):
    """Extract metadata using Large Language Models via Instructor."""

    def __init__(
        self,
        backend: str = DEFAULT_LLM_PROVIDER,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.0,
        max_retries: int = 3,
        **kwargs,
    ):
        raise NotImplementedError

    def _provider_env_key(self) -> Optional[str]:
        pass

    def _check_ollama_available(self) -> bool:
        """Check if ollama is installed and running."""
        pass

    def _initialize_client(self):
        pass

    def _create_extraction_prompt(
        self, text: str, fields: Optional[List[str]] = None
    ) -> str:
        """Create prompt for metadata extraction."""
        raise NotImplementedError

    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """Call the LLM backend with the prompt."""
        raise NotImplementedError

    def extract_metadata(
        self, text: str, fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract metadata from text using LLM.

        Args:
            text: Input text
            fields: List of fields to extract

        Returns:
            Dictionary with extracted metadata
        """
        raise NotImplementedError


class EmbeddingMetadataExtractor(MetadataExtractor):
    """Extract metadata using embedding-based similarity matching."""

    def __init__(
        self,
        model_name: str = "FremyCompany/BioLORD-2023",
        backend: str = "sentence-transformers",
        reference_categories: Dict[str, List[str]] = None,
        **kwargs,
    ):
        """
        Initialize embedding-based metadata extractor.

        Args:
            model_name: Embedding model name (default: FremyCompany/BioLORD-2023 - optimized for biomedical text)
            backend: Embedding backend ("sentence-transformers", "fastembed")
            reference_categories: Reference categories for classification (required)
            **kwargs: Additional parameters for embedding model

        Raises:
            ValueError: If reference_categories is not provided
        """
        raise NotImplementedError

    def _load_model(self):
        """Load the embedding model."""
        pass

    def _get_cache_path(self) -> str:
        """Get path for embedding cache file."""
        pass

    def _compute_reference_embeddings(self) -> Dict[str, Any]:
        """Compute embeddings for reference categories with caching."""
        pass

    def _find_best_match(
        self, text_embedding, category: str, threshold: float = 0.3
    ) -> str:
        """Find best matching category using cosine similarity."""
        raise NotImplementedError

    def _parse_structured_fields(self, text: str) -> Dict[str, str]:
        """
        Parse structured text in 'field: value' format.

        Args:
            text: Input text with potential 'field: value' patterns

        Returns:
            Dictionary of parsed field-value pairs
        """
        raise NotImplementedError

    def _match_value_or_text(
        self, value: Optional[str], full_text: str, category: str
    ) -> str:
        """
        Match a specific extracted value or fall back to full text matching.

        This method first tries to match an extracted value (e.g., "F" from "sex: F")
        directly against reference categories. If that fails or no value is provided,
        it falls back to matching the full combined text.

        Args:
            value: Extracted field value (e.g., "F" from "sex: F")
            full_text: Full combined text for fallback matching
            category: Category name to match against

        Returns:
            Best matching category value or "Unknown"
        """
        raise NotImplementedError

    def extract_metadata(
        self, text: str, fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Extract metadata using embedding similarity.

        Args:
            text: Input text
            fields: List of fields to extract

        Returns:
            Dictionary with extracted metadata
        """
        raise NotImplementedError


def create_metadata_extractor(
    method: str = "llm",
    backend: Optional[str] = None,
    model: Optional[str] = None,
    **kwargs,
) -> MetadataExtractor:
    """
    Factory function to create metadata extractor.

    Args:
        method: Extraction method (``llm`` or ``embedding``)
        backend: Backend for the method
        model: Model name
        kwargs: Additional parameters (as keyword arguments)

    Returns:
        MetadataExtractor instance

    Examples:
        >>> # LLM-based with Instructor (default provider)
        >>> extractor = create_metadata_extractor(method="llm")
        >>>
        >>> # Embedding-based (default: BioLORD-2023 for biomedical text)
        >>> extractor = create_metadata_extractor(method="embedding")
    """
    raise NotImplementedError


def apply_dataframe_enrichment(
    df: pd.DataFrame,
    method: str = "embedding",
    backend: Optional[str] = None,
    model: Optional[str] = None,
    text_column: Optional[str] = None,
    show_progress: bool = True,
    prefix: str = "guessed_",
) -> pd.DataFrame:
    """
    Utility function to apply metadata enrichment to a DataFrame.

    This is a convenience function that handles:
    - Column auto-detection
    - Extractor initialization
    - Error handling
    - Progress display

    Args:
        df: Input DataFrame
        method: Enrichment method ('llm' or 'embedding')
        backend: Backend for the method
        model: Model name
        text_column: Column to use (auto-detected if None)
        show_progress: Show progress bar
        prefix: Prefix for new columns

    Returns:
        Enriched DataFrame

    Example:
        >>> from pysradb.metadata_enrichment import apply_dataframe_enrichment
        >>> enriched_df = apply_dataframe_enrichment(
        ...     df,
        ...     method="embedding",
        ...     text_column="experiment_title"
        ... )
    """
    pass
