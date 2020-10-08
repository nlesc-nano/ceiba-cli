"""Library API."""

import logging

from .__version__ import __version__
from .actions import add_jobs, compute, query_properties, report, update_jobs
from .client import query_server

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Felipe Zapata"
__email__ = 'f.zapata@esciencecenter.nl'
