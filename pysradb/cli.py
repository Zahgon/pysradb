"""Command line interface for pysradb"""

import argparse
import os
import re
import sys
import warnings
from io import StringIO
from textwrap import dedent

import pandas as pd
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from . import __version__
from .exceptions import IncorrectFieldException, MissingQueryException
from .geoweb import GEOweb, download_geo_matrix, parse_geo_matrix_to_tsv
from .search import EnaSearch, GeoSearch, SraSearch
from .sraweb import SRAweb
from .utils import confirm

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

warnings.simplefilter(action="ignore", category=FutureWarning)

console = Console()


class CustomFormatterArgP(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        raise NotImplementedError


def pretty_print_df(df, include_header=True):
    """Pretty print dataframe using rich formatting"""

    def format_value(v):
        raise NotImplementedError

    raise NotImplementedError
def _create_table(df, terminal_width, include_header, format_value):
    """Helper function to create a rich table with appropriate sizing"""

    raise NotImplementedError


def _print_save_df(df, saveto=None):
    """Save dataframe to file or print with rich formatting.

    Automatically detects format from file extension:
    - .csv: Comma-separated values
    - .tsv: Tab-separated values
    - .txt: Tab-separated values (text format)
    - .json: JSON format
    """
    raise NotImplementedError


###################### metadata ##############################
def metadata(
    srp_id, assay, desc, detailed, expand, saveto, enrich=False, enrich_backend=None
):
    # Validate that at least one ID was provided
    raise NotImplementedError


################################################################


################# download ##########################
def download(
    out_dir,
    srx,
    srp,
    geo,
    skip_confirmation,
    col="public_url",
    use_ascp=False,
    threads=1,
):
    raise NotImplementedError


#########################################################


######################### search #################################
def search(saveto, db, verbosity, return_max, fields):
    raise NotImplementedError


def get_geo_search_info():
    raise NotImplementedError


####################################################################


######################### gse-to-gsm ###############################
def gse_to_gsm(gse_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


####################################################################


######################## gse-to-srp ################################
def gse_to_srp(gse_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


######################################################################


######################### gsm-to-gse #################################
def gsm_to_gse(gsm_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


########################################################################


############################ gsm-to-srp ################################
def gsm_to_srp(gsm_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


########################################################################


############################ gsm-to-srr ################################
def gsm_to_srr(gsm_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


########################################################################


############################ gsm-to-srs ################################
def gsm_to_srs(gsm_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


########################################################################


############################# gsm-to-srx ###############################
def gsm_to_srx(gsm_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srp-to-gse ##################################
def srp_to_gse(srp_id, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srp-to-srr ##################################
def srp_to_srr(srp_id, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srp-to-srs ##################################
def srp_to_srs(srp_id, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srp-to-srx ##################################
def srp_to_srx(srp_id, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srr-to-gsm ##################################
def srr_to_gsm(srr_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


########################################################################


########################### srr-to-srp ##################################
def srr_to_srp(srr_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srr-to-srs ##################################
def srr_to_srs(srr_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srr-to-srx ##################################
def srr_to_srx(srr_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srs-to-gsm ##################################
def srs_to_gsm(srs_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srs-to-srx ##################################
def srs_to_srx(srs_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srx-to-srp ##################################
def srx_to_srp(srx_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srx-to-srr ##################################
def srx_to_srr(srx_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


#########################################################################


########################### srx-to-srs ##################################
def srx_to_srs(srx_ids, saveto, detailed, desc, expand):
    raise NotImplementedError


def srp_to_pmid(srp_ids, saveto):
    raise NotImplementedError


def sra_to_pmid(sra_ids, saveto):
    """Backward compatibility wrapper for sra_to_pmid"""
    raise NotImplementedError


def gse_to_pmid(gse_ids, saveto):
    raise NotImplementedError


def pmid_to_gse(pmid_ids, saveto):
    raise NotImplementedError


def pmid_to_srp(pmid_ids, saveto):
    raise NotImplementedError


def pmc_to_identifiers(pmc_ids, saveto):
    raise NotImplementedError


def pmid_to_identifiers(pmid_ids, saveto):
    raise NotImplementedError


def doi_to_gse(doi_ids, saveto):
    raise NotImplementedError


def doi_to_srp(doi_ids, saveto):
    raise NotImplementedError


def doi_to_identifiers(doi_ids, saveto):
    raise NotImplementedError


#########################################################################


########################### geo-matrix ##################################
def geo_matrix(accession, to_tsv, output_dir):
    # Download the GEO Matrix file
    raise NotImplementedError


#########################################################################


def parse_args(args=None):
    """Argument parser"""
    raise NotImplementedError


if __name__ == "__main__":
    parse_args(sys.argv[1:])
