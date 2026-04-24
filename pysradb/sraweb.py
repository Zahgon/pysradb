"""Utilities to interact with SRA online"""

import concurrent.futures
import os
import re
import sys
import time
import warnings
from collections import OrderedDict
from json.decoder import JSONDecodeError
from xml.parsers.expat import ExpatError

import numpy as np
import pandas as pd
import requests
import xmltodict

warnings.simplefilter(action="ignore", category=FutureWarning)

from xml.sax.saxutils import escape


def xmlescape(data):
    pass


def _make_hashable(obj):
    """Convert unhashable types to hashable ones for pandas operations"""
    raise NotImplementedError


def _order_first(df, column_order_list):
    raise NotImplementedError


def _retry_response(base_url, payload, key, max_retries=10):
    """Rerty fetching esummary if API rate limit exceeeds"""
    raise NotImplementedError


def get_retmax(n_records, retmax=500):
    """Get retstart and retmax till n_records are exhausted"""
    raise NotImplementedError


class SRAweb(object):
    def __init__(self, api_key=None):
        """
        Initialize SRAweb for API-based access to SRA data.

        Parameters
        ----------

        api_key: string
                 API key for ncbi eutils. Optional, but recommended for higher rate limits.
        """
        raise NotImplementedError

    @staticmethod
    def format_xml(string):
        """Create a fake root to make 'string' a valid xml

        Parameters
        ----------
        string: str

        Returns
        --------
        xml: str
        """
        # string = unescape(string.strip())
        raise NotImplementedError

    @staticmethod
    def xml_to_json(xml):
        """Convert xml to json.

        Parameters
        ----------
        xml: str
             Input XML

        Returns
        -------
        xml_dict: dict
                  Parsed xml as dict
        """
        raise NotImplementedError

    def bioproject_to_srp(self, bioproject):
        """Convert PRJNA BioProject ID to SRP accession

        Parameters
        ----------
        bioproject: str
                   BioProject ID (e.g., 'PRJNA810439')

        Returns
        -------
        srp_accessions: list
                       List of SRP accessions found
        """
        raise NotImplementedError

    def fetch_ena_fastq(self, srp):
        """Fetch FASTQ records from ENA (EXPERIMENTAL)

        Parameters
        ----------
        srp: string
             Srudy accession

        Returns
        -------
        srr_url: list
                 List of SRR fastq urls
        """
        def _handle_url_split(url_split):
            raise NotImplementedError

        raise NotImplementedError
    def get_efetch_response(self, db, term, usehistory="y"):
        raise NotImplementedError

    def sra_metadata(
        self,
        srp,
        sample_attribute=False,
        detailed=False,
        expand_sample_attributes=False,
        output_read_lengths=False,
        include_pmids=False,
        enrich=False,
        enrich_backend="ollama/phi3",
        **kwargs,
    ):
        raise NotImplementedError

    def fetch_gds_results(self, gse, **kwargs):
        raise NotImplementedError

    def fetch_gsm_soft(self, gsm_ids):
        """
        Fetch detailed GSM metadata in SOFT format.

        Args:
            gsm_ids: List of GSM accessions

        Returns:
            Dictionary mapping GSM accession to parsed SOFT metadata
        """
        raise NotImplementedError

    def geo_metadata(
        self,
        gse,
        sample_attribute=False,
        detailed=False,
        expand_sample_attributes=False,
        include_pmids=False,
        enrich=False,
        enrich_backend="ollama/phi3",
        **kwargs,
    ):
        def get_fastq_url(row):
            raise NotImplementedError

        raise NotImplementedError

    def metadata(self, accession, **kwargs):
        """
        Unified method to fetch metadata for SRA or GEO accessions.

        Automatically detects accession type and calls appropriate method.

        Args:
            accession: ``SRP``/``GSE`` accession(s) - can be string or list
            kwargs: Additional parameters passed to ``sra_metadata()`` or ``geo_metadata()``
                     (e.g., ``detailed``, ``enrich``, ``enrich_backend``, ``sample_attribute``, etc.)

        Returns:
            DataFrame with metadata (enriched if enrich=True)

        Examples:
            >>> client = SRAweb()
            >>> df = client.metadata("GSE286254", detailed=True, enrich=True)
            >>> df = client.metadata("SRP253951", detailed=True, enrich=True)
            >>> df = client.metadata(["GSE286254", "GSE147507"], enrich=True)
        """
        raise NotImplementedError

    def gse_to_gsm(self, gse, **kwargs):
        raise NotImplementedError

    def gse_to_srp(self, gse, **kwargs):
        raise NotImplementedError

    def gsm_to_srp(self, gsm, **kwargs):
        raise NotImplementedError

    def gsm_to_srr(self, gsm, **kwargs):
        raise NotImplementedError

    def gsm_to_srs(self, gsm, **kwargs):
        """Get SRS for a GSM"""
        raise NotImplementedError

    def gsm_to_srx(self, gsm, **kwargs):
        """Get SRX for a GSM"""
        raise NotImplementedError

    def gsm_to_gse(self, gsm, **kwargs):
        raise NotImplementedError

    def srp_to_gse(self, srp, **kwargs):
        """Get GSE for a SRP"""
        raise NotImplementedError

    def srp_to_srr(self, srp, **kwargs):
        """Get SRR for a SRP"""
        raise NotImplementedError

    def srp_to_srs(self, srp, **kwargs):
        """Get SRS for a SRP"""
        raise NotImplementedError

    def srp_to_srx(self, srp, **kwargs):
        """Get SRX for a SRP"""
        raise NotImplementedError

    def srr_to_gsm(self, srr, **kwargs):
        """Get GSM for a SRR"""
        raise NotImplementedError

    def srr_to_srp(self, srr, **kwargs):
        """Get SRP for a SRR"""
        raise NotImplementedError

    def srr_to_srs(self, srr, **kwargs):
        """Get SRS for a SRR"""
        raise NotImplementedError

    def srr_to_srx(self, srr, **kwargs):
        """Get SRX for a SRR"""
        raise NotImplementedError

    def srs_to_gsm(self, srs, **kwargs):
        """Get GSM for a SRS"""
        raise NotImplementedError

    def srx_to_gsm(self, srx, **kwargs):
        raise NotImplementedError

    def srs_to_srx(self, srs, **kwargs):
        """Get SRX for a SRS"""
        raise NotImplementedError

    def srx_to_srp(self, srx, **kwargs):
        """Get SRP for a SRX"""
        raise NotImplementedError

    def srx_to_srr(self, srx, **kwargs):
        """Get SRR for a SRX"""
        raise NotImplementedError

    def srx_to_srs(self, srx, **kwargs):
        """Get SRS for a SRX"""
        raise NotImplementedError

    def search(self, *args, **kwargs):
        raise NotImplementedError("Search not yet implemented for Web")

    def fetch_bioproject_pmids(self, bioprojects):
        """Fetch PMIDs for given BioProject accessions

        Parameters
        ----------
        bioprojects: list or str
                    BioProject accession(s)

        Returns
        -------
        bioproject_pmids: dict
                         Mapping of BioProject to list of PMIDs
        """
        raise NotImplementedError

    def srp_to_pmid(self, srp_accessions):
        """Get PMIDs associated with SRP accessions

        Parameters
        ----------
        srp_accessions: list or str
                       SRP accession(s)

        Returns
        -------
        srp_pmid_df: pandas.DataFrame
                    DataFrame with SRP accessions and associated PMIDs
        """
        raise NotImplementedError

    def _search_fallback_pmids(self, srp_accessions):
        """Search for PMIDs using fallback strategies (external sources + direct SRA search + GSE search)"""
        raise NotImplementedError

    def _extract_sra_accession(self, row):
        """Extract SRA accession from metadata row"""
        raise NotImplementedError

    def _get_smallest_pmid(self, pmids):
        """Get the numerically smallest PMID from a list"""
        raise NotImplementedError

    def extract_external_sources(self, metadata_df):
        """Extract external source identifiers from SRA metadata

        Parameters
        ----------
        metadata_df: pandas.DataFrame
                    DataFrame containing SRA metadata

        Returns
        -------
        external_sources: list
                         List of external source identifiers found
        """
        raise NotImplementedError

    def _search_gse_gsm_pmids(self, metadata_df, sra_accessions):
        """Search for PMIDs using GSE identifiers from BioProject and SRP conversion

        Parameters
        ----------
        metadata_df: pandas.DataFrame
                    Detailed metadata DataFrame
        sra_accessions: list
                       List of SRA accessions being searched

        Returns
        -------
        pmids: list
              List of PMIDs found via GSE search
        """
        raise NotImplementedError

    def _bioproject_to_gse(self, bioproject):
        """Convert BioProject ID to GSE ID via NCBI search

        Parameters
        ----------
        bioproject: str
                   BioProject ID (e.g., 'PRJNA1065472')

        Returns
        -------
        gse_ids: list
                List of GSE IDs found
        """
        raise NotImplementedError

    def _srp_to_gse_via_elink(self, srp_id):
        """Convert SRP ID to GSE ID via NCBI ELink

        Parameters
        ----------
        srp_id: str
               SRP ID (e.g., 'SRP484103')

        Returns
        -------
        gse_ids: list
                List of GSE IDs found
        """
        raise NotImplementedError

    def _search_pmc_by_bioproject(self, bioproject_id):
        """Search PubMed Central for PMIDs using BioProject accession ID

        This provides a fallback mechanism when the BioProject XML doesn't contain
        publication metadata but the research has been published and is cited in PMC.

        Parameters
        ----------
        bioproject_id: str
                      BioProject accession ID (e.g., PRJEB39301, PRJNA123456)

        Returns
        -------
        pmids: list
              List of PMIDs found associated with the bioproject
        """
        raise NotImplementedError

    def search_pmc_for_external_sources(self, external_sources):
        """Search PubMed Central for PMIDs using external source identifiers

        Parameters
        ----------
        external_sources: list
                         List of external source identifiers

        Returns
        -------
        pmids: list
              List of PMIDs found
        """
        raise NotImplementedError

    def sra_to_pmid(self, sra_accessions):
        """Get PMIDs for SRA accessions (backward compatibility wrapper)

        Parameters
        ----------
        sra_accessions: list or str
                       SRA accession(s) - can be SRP, SRR, SRX, or SRS

        Returns
        -------
        sra_pmid_df: pandas.DataFrame
                    DataFrame with SRA accessions and associated PMIDs
        """
        # For SRP accessions, use the main method
        raise NotImplementedError

    def srr_to_pmid(self, srr):
        """Get PMIDs for Run Accessions (SRR)"""
        pass

    def srx_to_pmid(self, srx):
        """Get PMIDs for Experiment Accessions (SRX)"""
        pass

    def srs_to_pmid(self, srs):
        """Get PMIDs for Sample Accessions (SRS)"""
        pass

    def gse_to_pmid(self, gse_accessions):
        """Get PMIDs for GSE accessions by searching PubMed Central

        Parameters
        ----------
        gse_accessions: list or str
                       GSE accession(s)

        Returns
        -------
        gse_pmid_df: pandas.DataFrame
                    DataFrame with GSE accessions and associated PMIDs
        """
        raise NotImplementedError

    def doi_to_pmid(self, dois):
        """Convert DOI(s) to PMID(s)

        Parameters
        ----------
        dois: list or str
             DOI(s)

        Returns
        -------
        doi_pmid_mapping: dict
                         Mapping of DOI to PMID
        """
        raise NotImplementedError

    def pmid_to_pmc(self, pmids):
        """Convert PMID(s) to PMC ID(s)

        Parameters
        ----------
        pmids: list or str
              PMID(s)

        Returns
        -------
        pmid_pmc_mapping: dict
                         Mapping of PMID to PMC ID
        """
        raise NotImplementedError

    def fetch_pmc_fulltext(self, pmc_id):
        """Fetch full text from PMC article

        Parameters
        ----------
        pmc_id: str
               PMC ID (can be with or without 'PMC' prefix)

        Returns
        -------
        fulltext: str
                 Full text of the article, or None if unavailable
        """
        # Ensure PMC ID has the PMC prefix
        raise NotImplementedError

    def extract_identifiers_from_text(self, text):
        """Extract GSE, PRJNA, SRP, and other identifiers from text

        Parameters
        ----------
        text: str
             Text to search for identifiers

        Returns
        -------
        identifiers: dict
                    Dictionary with lists of found identifiers by type
        """
        raise NotImplementedError

    def pmc_to_identifiers(self, pmc_ids, convert_missing=True):
        """Extract database identifiers from PMC articles

        Parameters
        ----------
        pmc_ids: list or str
                PMC ID(s) (can be with or without 'PMC' prefix)
        convert_missing: bool
                        If True, automatically convert GSE↔SRP when one is found but not the other
                        Default: True

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with PMC IDs and extracted identifiers
        """
        raise NotImplementedError

    def pmid_to_identifiers(self, pmids):
        """Extract database identifiers from PubMed articles via PMC

        Parameters
        ----------
        pmids: list or str
              PMID(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with PMIDs, PMC IDs, and extracted identifiers
        """
        raise NotImplementedError

    def pmid_to_gse(self, pmids):
        """Get GSE identifiers from PMID(s)

        Parameters
        ----------
        pmids: list or str
              PMID(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with PMIDs and GSE identifiers
        """
        raise NotImplementedError

    def pmid_to_srp(self, pmids):
        """Get SRP identifiers from PMID(s)

        Parameters
        ----------
        pmids: list or str
              PMID(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with PMIDs and SRP identifiers
        """
        raise NotImplementedError

    def doi_to_identifiers(self, dois):
        """Extract database identifiers from articles via DOI

        Parameters
        ----------
        dois: list or str
             DOI(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with DOIs, PMIDs, PMC IDs, and extracted identifiers
        """
        raise NotImplementedError

    def doi_to_gse(self, dois):
        """Get GSE identifiers from DOI(s)

        Parameters
        ----------
        dois: list or str
             DOI(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with DOIs and GSE identifiers
        """
        raise NotImplementedError

    def doi_to_srp(self, dois):
        """Get SRP identifiers from DOI(s)

        Parameters
        ----------
        dois: list or str
             DOI(s)

        Returns
        -------
        results_df: pandas.DataFrame
                   DataFrame with DOIs and SRP identifiers
        """
        raise NotImplementedError
