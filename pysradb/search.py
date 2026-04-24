"""This file contains the search classes for the search feature."""

import os
import re
import sys
import time
import urllib
import xml.etree.ElementTree as Et
from json import JSONDecodeError

import pandas as pd
import requests
from tqdm.autonotebook import tqdm

from .exceptions import IncorrectFieldException, MissingQueryException
from .utils import requests_3_retries, scientific_name_to_taxid

SEARCH_REQUEST_TIMEOUT = 20
SRA_SEARCH_GROUP_SIZE = 300


class QuerySearch:
    """This is the base class for the search feature.

    This class takes as input the user's search query, which has been
    tokenized by the ArgParser. The query will be sent to either SRA or ENA
    depending on the user's input, and the results will be returned as a
    pandas dataframe.

    Attributes
    ----------
    self.df: Pandas DataFrame
        The search result belonging to this search instance

    Parameters
    ----------
    verbosity : integer
        The level of details of the search result.
    return_max : int
        The maximum number of entries to be returned.
    query : str
        The main query string.
    accession : str
        A relevant study / experiment / sample / run accession number.
    organism  : str
        Scientific name of the sample organism
    layout : str
        Library layout. Possible inputs: single, paired
    mbases : int
        Size of the sample of interest rounded to the nearest megabase.
    publication_date : str
        The publication date of the run in the format dd-mm-yyyy. If a
        date range is desired, input should be in the format of
        dd-mm-yyyy:dd-mm-yyyy
    platform : str
        Sequencing platform used for the run. Some possible inputs include:
        illumina, ion torrent, oxford nanopore
    selection : str
        Library selection. Some possible inputs: cdna, chip, dnase, pcr
    source : str
        Library source. Some possible inputs: genomic, metagenomic,
        transcriptomic
    strategy : str
        Library Preparation strategy. Some possible inputs: wgs, amplicon,
        rna seq
    title : str
        Title of the experiment associated with the run
    suppress_validation: bool
        Defaults to False. If this is set to True, the user input format
        checks will be skipped.
        Setting this to True may cause the program to behave in unexpected
        ways, but allows the user to search queries that does not pass the
        format check.

    Methods
    -------
    get_df()
        Returns the dataframe storing this search result.

    search()
        Executes the search.

    show_result_statistics()
        Shows summary information about search results.

    visualise_results()
        Generate graphs that visualise the search results.

    get_plot_objects():
        Get the plot objects for plots generated.

    """

    def __init__(
        self,
        verbosity=2,
        return_max=20,
        query=None,
        accession=None,
        organism=None,
        layout=None,
        mbases=None,
        publication_date=None,
        platform=None,
        selection=None,
        source=None,
        strategy=None,
        title=None,
        suppress_validation=False,
    ):
        raise NotImplementedError

    def _input_multi_regex_checker(self, regex_matcher, input_query, error_message):
        """Checks if the user input match exactly 1 of the possible regex.

        This is a helper method for _validate_fields. It takes as input a
        dictionary of regex expression : accepted string by API pairs, and
        an input string, and verifies that the input string matches exactly
        one of the regex expressions.
        Matching multiple expressions indicates the input string is
        ambiguous, while matching none of the expressions suggests the
        input will likely produce no results or an error.
        Once matched, this method formats the user input so that it
        can be accepted by the API to be queried, as ENA especially expect
        case-sensitive exact matches for search queries.

        Parameters
        ----------
        regex_matcher : dict
            dictionary of regex expression : accepted string by API pairs.
        input_query : str
            input string for a particular query field.
        error_message : str
            error message to be shown if input_query does not match any of
            the regex expressions in regex_matcher.

        Returns
        -------
        tuple
            tuple pair of (input_query, message).
            message is "" if no format error has been identified, error
            message otherwise.
        """
        pass

    def _validate_fields(self):
        """Verifies that user input format is correct.

        This helper function tries to match the input query strings from
        the user to the exact string that is accepted by both SRA and ENA

        Note: as of the implementation of this method, ENA does not have
        a documentation page listing the accepted values for query
        parameters. The list of parameters below were collected from ENA's
        advanced search page: https://www.ebi.ac.uk/ena/browser/advanced-search

        Updating new values:
        If any new values are accepted by ENA, it should appear under
        the corresponding parameter in the page. To update this method,
        think of a regex that captures what the user may type for the new
        value, and include it in the respective xxx_matcher dictionary
        below as a regex:value key value pair.

        Eg: if a new sequencing platform, Pokemon, is added to ENA,
        navigate to "Instrument Platform" parameter on ENA's advanced
        search page and copy the corresponding phrase (eg "poKe_Mon").
        Then add the key value pair ".*poke.*": "poKe_Mon" to
        platform_matcher below.

        Unlike SRA, ENA requires supplied param values to be exact match
        to filter accordingly (eg "cDNA_oligo_dT"), which motivated this
        feature.

        Raises
        ------
        IncorrectFieldException
            If the input to any query field is in the wrong format

        """
        pass

    def _list_stat(self, stat_header):
        raise NotImplementedError

    def show_result_statistics(self):
        """Shows search result statistics."""
        raise NotImplementedError

    def visualise_results(
        self, graph_types=("all",), show=False, saveto="./search_plots/"
    ):
        """Generate graphs that visualise the search results.

        This method will only work if the optional dependency, matplotlib,
        is installed in the system.

        Parameters
        ----------
        graph_types : tuple
            tuple containing strings representing types of graphs to
            generate.
            Possible strings: all, daterange, organism, source, selection, platform,
            basecount
        saveto : str
            directory name where the generated graphs are saved.

        show : bool
            Whether plotted graphs are immediately shown.
        """
        raise NotImplementedError

    def search(self):
        pass

    def get_df(self):
        """Getter for the search result dataframe."""
        raise NotImplementedError

    def get_plot_objects(self):
        """Get the plot objects for plots generated."""
        pass

    def _plot_graph(self, plt, axes, show, savedir, too_many_organisms):
        """Plots a graph based on data from self.stats

        Parameters
        ----------
        axes: tuple
            tuple containing 1 or 2 strings corresponding to the statistics
            to plot. 1 string: Histogram. 2 string: heat map
        savedir: str
            directory to save to
        show: bool
            whether to call plt.show
        """
        raise NotImplementedError


class SraSearch(QuerySearch):
    """Subclass of QuerySearch that implements search by querying
    NCBI Entrez API

    Methods
    -------
    search()
        sends the user query via requests to NCBI Entrez API and returns
        search results as a pandas dataframe.

    show_result_statistics()
        Shows summary information about search results.

    visualise_results()
        Generate graphs that visualise the search results.

    get_plot_objects():
        Get the plot objects for plots generated.

    get_uids():
        Get NCBI uids retrieved during this search query.

    _format_query_string()
        formats the input user query into a string

    _format_request()
        formats the request payload

    _format_result(content)
        formats the search query output.

    See Also
    --------
    QuerySearch: Superclass of SraSearch

    """

    def __init__(
        self,
        verbosity=2,
        return_max=20,
        query=None,
        accession=None,
        organism=None,
        layout=None,
        mbases=None,
        publication_date=None,
        platform=None,
        selection=None,
        source=None,
        strategy=None,
        title=None,
        suppress_validation=False,
    ):
        raise NotImplementedError

    def search(self):
        # Step 1: retrieves the list of uids that satisfies the input
        # search query
        raise NotImplementedError

    def get_uids(self):
        """Get NCBI uids retrieved during this search query.

        Note: There is a chance that some uids retrieved do not appear in
        the search result output (Refer to #88)
        """
        pass

    def _format_query_string(self):
        raise NotImplementedError

    def _format_request(self):
        raise NotImplementedError

    def _format_response(self, content):
        raise NotImplementedError

    def _format_result(self):
        raise NotImplementedError

    def _parse_entry(self, entry_root):
        """Parses a subset of the XML tree from request stream

        Parameters
        ----------
        entry_root: ElementTree.Element
            root element of the xml tree from requests stream
        """
        raise NotImplementedError

    def _update_entry(self, field_name, field_content):
        """Adds information from a field into the entries dictionary

        This is a helper function that adds information parsed from the XML
        output from SRA into a dictionary of lists, for easier conversion
        into a Pandas dataframe later. Dictionary key is created if it
        doesn't exist yet. For entries that does not have information
        belonging to a field, the corresponding list will be padded with
        empty strings.

        Parameters
        ----------
        field_name: str
            Name of the field where a value belonging to an entry is to be
            added
        field_content: str
            Value to be added
        """
        raise NotImplementedError

    def _update_stats(self):
        # study
        raise NotImplementedError

    def _merge_selected_columns(self, regex):
        raise NotImplementedError


class EnaSearch(QuerySearch):
    """Subclass of QuerySearch that implements search via querying ENA API


    Methods
    -------
    search()
        sends the user query via requests to ENA API and stores search
        result as an instance attribute in the form of a pandas dataframe

    show_result_statistics()
        Shows summary information about search results.

    visualise_results()
        Generate graphs that visualise the search results.

    get_plot_objects():
        Get the plot objects for plots generated.

    _format_query_string()
        formats the input user query into a string

    _format_request()
        formats the request payload

    _format_result(content)
        formats the search query output and converts it into a pandas
        dataframe

    See Also
    --------
    QuerySearch: Superclass of EnaSearch

    """

    def search(self):
        # This ensures that the spaces in the query string are not
        # converted to '+' by requests.
        raise NotImplementedError

    def _format_query_string(self):
        raise NotImplementedError

    def _format_request(self):
        # Note: ENA's API does not support searching a query in all fields.
        # Currently, if the user does not specify a query field, the query will
        # be matched to experiment_title (aka description),
        # or one of the accession fields
        raise NotImplementedError

    def _format_result(self, content):
        raise NotImplementedError

    def _update_stats(self):
        # study
        raise NotImplementedError


class GeoSearch(SraSearch):
    """Subclass of SraSearch that can query both GEO DataSets and SRA API.

    Methods
    -------
    search()
        sends the user query via requests to SRA, GEO DataSets, or both
        depending on the search query. If query is sent to both APIs,
        the intersection of the two sets of query results are returned.

    show_result_statistics()
        Shows summary information about search results.

    visualise_results()
        Generate graphs that visualise the search results.

    get_plot_objects():
        Get the plot objects for plots generated.

    _format_geo_query_string()
        formats the GEO DataSets portion of the input user query into a
        string.

    _format_geo_request()
        formats the GEO DataSets request payload

    _format_result(content)
        formats the search query output and converts it into a pandas
        dataframe

    See Also
    --------
    GeoSearch.info: GeoSearch usage details
    SraSearch: Superclass of GeoSearch
    QuerySearch: Superclass of SraSearch

    """

    def __init__(
        self,
        verbosity=2,
        return_max=20,
        query=None,
        accession=None,
        organism=None,
        layout=None,
        mbases=None,
        publication_date=None,
        platform=None,
        selection=None,
        source=None,
        strategy=None,
        title=None,
        geo_query=None,
        geo_dataset_type=None,
        geo_entry_type=None,
        suppress_validation=False,
    ):
        raise NotImplementedError

    def _format_geo_query_string(self):
        raise NotImplementedError

    def _format_geo_request(self):
        raise NotImplementedError

    def _format_request(self):
        raise NotImplementedError

    def search(self):
        """Sends the user query via requests to SRA, GEO DataSets, or both"""
        raise NotImplementedError

    def _combine_uids(self, uids_from_sra, uids_from_geo):
        """Combine SRA and GEO uid lists while preserving ordering stability."""
        raise NotImplementedError

    @classmethod
    def info(cls):
        """Information on how to use GeoSearch.

        Displays information on how to query GEO DataSets / SRA via
        GeoSearch, including accepted inputs for geo_query,
        geo_dataset_type and geo_entry_type.

        Returns
        -------
        info: str
            Information on how to use GeoSearch.
        """
        raise NotImplementedError
