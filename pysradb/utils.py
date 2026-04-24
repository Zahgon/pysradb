import errno
import gzip
import io
import ntpath
import os
import shlex
import subprocess
import urllib.request as urllib_request
import warnings

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

warnings.filterwarnings("ignore", category=UserWarning, module="tqdm")
from tqdm.autonotebook import tqdm

from .exceptions import IncorrectFieldException

warnings.simplefilter(action="ignore", category=FutureWarning)


tqdm.pandas()


def path_leaf(path):
    """Get path's tail from a filepath.

    Parameters
    ----------
    path: string
          Filepath

    Returns
    -------
    tail: string
          Filename
    """
    pass


def requests_3_retries():
    """Generates a requests session object that allows 3 retries.

    Returns
    -------
    session: requests.Session
        requests session object that allows 3 retries for server-side
        errors.
    """
    raise NotImplementedError


def scientific_name_to_taxid(name):
    """Converts a scientific name to its corresponding taxonomy ID.

    Parameters
    ----------
    name: str
        Scientific name of interest.

    Returns
    -------
    taxid: str
        Taxonomy Id of the Scientific name.

    Raises
    ------
    IncorrectFieldException
        If the scientific name cannot be found.

    """

    raise NotImplementedError


def unique(sequence):
    """Get unique elements from a list maintaining the order.

    Parameters
    ----------
    input_list: list

    Returns
    -------
    unique_list: list
                 List with unique elements maintaining the order
    """
    raise NotImplementedError


class TqdmUpTo(tqdm):
    """Alternative Class-based version of the above.
    Provides `update_to(n)` which uses `tqdm.update(delta_n)`.
    Inspired by [twine#242](https://github.com/pypa/twine/pull/242),
    [here](https://github.com/pypa/twine/commit/42e55e06).

    Credits:
    https://github.com/tqdm/tqdm/blob/69326b718905816bb827e0e66c5508c9c04bc06c/examples/tqdm_wget.py
    """

    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        pass


def _extract_first_field(data):
    """Extract first field from a list of fields."""
    pass


def _find_aspera_keypath(aspera_dir=None):
    """Locate aspera key.

    Parameters
    ----------
    aspera_dir: string
                Location to aspera directory (optional)

    Returns
    -------
    aspera_keypath: string
                    Location to aspera key
    """
    pass


def mkdir_p(path):
    """Python version mkdir -p

    Parameters
    ----------
    path : string
           Path to directory to create
    """
    raise NotImplementedError


def order_dataframe(df, columns):
    """Order a dataframe

    Order a dataframe by moving the `columns` in the front

    Parameters
    ----------
    df: Dataframe
        Dataframe
    columns: list
             List of columns that need to be put in front
    """
    pass


def _get_url(url, download_to, show_progress=True):
    """Download anything at a given url.

    Parameters
    ----------
    url: string
         http/https/ftp url
    download_to: string
                 File location to write the downloaded file to
    show_progress: bool
                   Set to True by default to print progress bar
    """
    raise NotImplementedError


def run_command(command, verbose=False):
    """Run a shell command"""
    pass


def get_gzip_uncompressed_size(filepath):
    """Get uncompressed size of a .gz file

    Parameters
    ----------
    filepath: string
              Path to input file

    Returns
    -------
    filesize: int
              Uncompressed file size
    """
    raise NotImplementedError


def confirm(preceeding_text):
    """Confirm user input.

    Parameters
    ----------
    preceeding_text: str
                     Text to print

    Returns
    -------
    response: bool
    """
    raise NotImplementedError


def copyfileobj(fsrc, fdst, bufsize=16384, filesize=None, desc=""):
    """Copy file object with a progress bar.

    Parameters
    ----------
    fsrc: filehandle
          Input file handle
    fdst: filehandle
          Output file handle
    bufsize: int
             Length of output buffer
    filesize: int
              Input file file size
    desc: string
          Description for tqdm status
    """
    raise NotImplementedError
