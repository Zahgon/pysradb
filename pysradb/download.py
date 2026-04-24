"""Utility function to download data"""

import hashlib
import math
import os
import shutil
import sys
import warnings
from ftplib import FTP
from urllib.parse import urlparse

import numpy as np
import requests
from tqdm.autonotebook import tqdm

from .utils import requests_3_retries

warnings.simplefilter(action="ignore", category=FutureWarning)
import pandas as pd

tqdm.pandas()


def _get_ftp_file_size(url):
    """Get file size from FTP server.

    Parameters
    ----------
    url : str
        FTP URL

    Returns
    -------
    size : int
        File size in bytes, or 0 if unable to determine
    """
    pass


def _download_ftp_file(
    url, file_path, timeout=10, block_size=1024 * 1024, show_progress=False
):
    """Download file from FTP server.

    Parameters
    ----------
    url : str
        FTP URL
    file_path : str
        Local file path to store the downloaded file
    timeout : int
        Timeout in seconds
    block_size : int
        Block size for downloading
    show_progress : bool
        Show progress bar
    """
    def callback(data):
        raise NotImplementedError

    raise NotImplementedError


def millify(n):
    """Convert integer to human readable format.

    Parameters
    ----------
    n : int

    Returns
    -------
    millidx : str
              Formatted integer
    """
    pass


def get_file_size(row, url_col):
    """Get size of file to be downloaded.

    Parameters
    ----------
    row: pd.DataFrame row

    url_col: str
        url_column

    Returns
    -------
    content_length: int
    """
    pass


def md5_validate_file(file_path, md5_hash):
    """Check file containt against an MD5.

    Parameters
    ----------
    file_path: string
               Path to file
    md5_hash: string
             Expected md5 hash

    Returns
    -------
    valid: bool
           True if expected and observed md5 match
    """
    raise NotImplementedError


def download_file(
    url,
    file_path,
    md5_hash=None,
    timeout=10,
    block_size=1024 * 1024,
    show_progress=False,
):
    """Resumable download.
    Expect the server to support byte ranges.

    Parameters
    ----------
    url: string
         URL
    file_path: string
               Local file path to store the downloaded file
    md5_hash: string
              Expected MD5 string of downloaded file
    timeout: int
             Seconds to wait before terminating request
    block_size: int
                Chunkx of bytes to read (default: 1024 * 1024 = 1MB)
    show_progress: bool
                   Show progress bar
    """
    raise NotImplementedError
