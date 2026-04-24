import re
import warnings

import numpy as np
import pandas as pd


def _get_sample_attr_keys(sample_attribute):
    raise NotImplementedError


def expand_sample_attribute_columns(metadata_df):
    """Expand sample attribute columns to individual columns.

    Since the sample_attribute column content can be different
    for differnt rows even if coming from the same project (SRP),
    we explicitly iterate through the rows to first determine
    what additional columns need to be created.


    Parameters
    ----------
    metadata_df: DataFrame
                 Dataframe as obtained from sra_metadata
                 or equivalent

    Returns
    -------
    expanded_df: DataFrame
                 Dataframe with additionals columns pertaining
                 to sample_attribute appended
    """
    raise NotImplementedError


def guess_cell_type(sample_attribute):
    """Guess possible cell line from sample_attribute data.

    Parameters
    ----------
    sample_attribute: string
                      sample_attribute string as in the metadata column

    Returns
    -------
    cell_type: string
               Possible cell type of sample.
               Returns None if no match found.
    """
    pass


def guess_tissue_type(sample_attribute):
    """Guess tissue type from sample_attribute data.

    Parameters
    ----------
    sample_attribute: string
                      sample_attribute string as in the metadata column

    Returns
    -------
    tissue_type: string
               Possible cell type of sample.
               Returns None if no match found.
    """
    pass


def guess_strain_type(sample_attribute):
    """Guess strain type from sample_attribute data.

    Parameters
    ----------
    sample_attribute: string
                      sample_attribute string as in the metadata column

    Returns
    -------
    strain_type: string
                 Possible cell type of sample.
                 Returns None if no match found.
    """
    pass
