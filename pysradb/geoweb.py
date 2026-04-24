"""Utilities to interact with GEO online"""

import gzip
import os
import re
import sys
from io import StringIO

import pandas as pd
import requests
from lxml import html

from .download import download_file
from .utils import _get_url, copyfileobj, get_gzip_uncompressed_size

PY3 = True
if sys.version_info[0] < 3:
    PY3 = False


class GEOweb(object):
    def __init__(self):
        """Initialize GEOweb without any database."""

    def get_download_links(self, gse):
        """Obtain all links from the GEO FTP page.

        Parameters
        ----------
        gse: string
             GSE ID

        Returns
        -------
        links: list
               List of all valid downloadable links present for a GEO ID
        """
        raise NotImplementedError

    def download(self, links, root_url, gse, verbose=False, out_dir=None):
        """Download GEO files.

        Parameters
        ----------
        links: list
               List of all links valid downloadable present for a GEO ID
        root_url: string
                  url for root directory for a GEO ID
        gse: string
             GEO ID
        verbose: bool
                 Print file list
        out_dir: string
                 Directory location for download
        """
        raise NotImplementedError


def download_geo_matrix(accession, output_dir="."):
    """
    Download a GEO Matrix file for a given GEO accession ID.

    Args:
        accession (str): GEO accession ID (e.g., 'GSE234190').
        output_dir (str): Directory to save the downloaded file (default: current directory).

    Returns:
        str: Path to the downloaded file.

    Raises:
        Exception: If the download fails.
    """
    # Construct the URL for the GEO Matrix file
    raise NotImplementedError


def parse_geo_matrix_to_tsv(input_file, output_file):
    """
    Parse a GEO Matrix file to a TSV file, extracting the expression data.

    Args:
        input_file (str): Path to the input GEO Matrix file (gzipped).
        output_file (str): Path to save the output TSV file.

    Returns:
        pandas.DataFrame: The parsed expression data.
    """
    # Read the gzipped file and extract the data section
    raise NotImplementedError
