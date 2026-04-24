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
    parsed = urlparse(url)
    tmp_file_path = file_path + ".part"

    # Check if partial file exists
    first_byte = os.path.getsize(tmp_file_path) if os.path.exists(tmp_file_path) else 0
    file_mode = "ab" if first_byte else "wb"

    try:
        ftp = FTP(parsed.netloc, timeout=timeout)
        ftp.login()

        file_size = ftp.size(parsed.path)
        if file_size is None:
            file_size = -1

        if show_progress and file_size > 0:
            desc = "Downloading {}".format(url.split("/")[-1])
            pbar = tqdm(
                total=file_size,
                initial=first_byte,
                unit="B",
                unit_scale=True,
                desc=desc,
            )

        with open(tmp_file_path, file_mode) as f:
            if first_byte > 0:
                ftp.voidcmd(f"REST {first_byte}")

            def callback(data):
                pass

            ftp.retrbinary(f"RETR {parsed.path}", callback, blocksize=block_size)

        if show_progress and file_size > 0:
            pbar.close()

        ftp.quit()

        if file_size == -1 or file_size == os.path.getsize(tmp_file_path):
            shutil.move(tmp_file_path, file_path)
        else:
            raise Exception(
                f"Download incomplete: expected {file_size} bytes, got {os.path.getsize(tmp_file_path)} bytes"
            )

    except Exception as e:
        if show_progress and "pbar" in locals():
            pbar.close()
        raise Exception(f"FTP download failed: {e}")


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
    observed_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            # read 1MB
            chunk = f.read(1000 * 1000)
            if not chunk:
                break
            observed_md5.update(chunk)
    return observed_md5.hexdigest() == md5_hash


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
    if url.startswith("ftp."):
        url = "ftp://" + url

    if os.path.exists(file_path) and os.path.getsize(file_path):
        return

    if url.startswith("ftp://"):
        _download_ftp_file(url, file_path, timeout, block_size, show_progress)
        # if there's a hash value, validate the file
        if md5_hash and not md5_validate_file(file_path, md5_hash):
            raise Exception("Error validating the file against its MD5 hash")
        return

    session = requests
    tmp_file_path = file_path + ".part"
    first_byte = os.path.getsize(tmp_file_path) if os.path.exists(tmp_file_path) else 0
    file_mode = "ab" if first_byte else "wb"
    file_size = -1
    try:
        file_size = int(session.head(url).headers["Content-length"])
        headers = {"Range": "bytes=%s-" % first_byte}
        r = session.get(url, headers=headers, stream=True)
        if show_progress:
            desc = "Downloading {}".format(url.split("/")[-1])
            pbar = tqdm(
                total=file_size,
                initial=first_byte,
                unit="B",
                unit_scale=True,
                desc=desc,
            )
        with open(tmp_file_path, file_mode) as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    if show_progress:
                        pbar.update(len(chunk))
        if show_progress:
            pbar.close()
    except IOError as e:
        sys.stderr.write("IO Error - {}\n".format(e))
    finally:
        # Move the temp file to desired location
        if os.path.exists(tmp_file_path):
            actual_size = os.path.getsize(tmp_file_path)
            if file_size == actual_size:
                if md5_hash and not md5_validate_file(tmp_file_path, md5_hash):
                    raise Exception("Error validating the file against its MD5 hash")
                shutil.move(tmp_file_path, file_path)
            elif file_size == -1:
                # Server didn't provide Content-Length, move the file anyway
                shutil.move(tmp_file_path, file_path)
            else:
                print(
                    f"Warning: File size mismatch for {url}. Expected: {file_size}, Got: {actual_size}"
                )
                if actual_size > 0:
                    shutil.move(tmp_file_path, file_path)
