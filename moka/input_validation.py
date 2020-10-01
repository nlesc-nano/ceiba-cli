"""Module to validate the user's input."""

import getpass
from pathlib import Path
from typing import Iterable

import yaml
from schema import And, Optional, Or, Schema, SchemaError, Use

from .utils import Options


def any_lambda(array: Iterable[str]) -> Schema:
    """Create an schema checking that the keyword matches one of the expected values."""
    return And(
        str, Use(str.lower), lambda s: s in array)


SCHEMA_SCHEDULER = Schema({
    Optional("name", default="none"): And(
        str, Use(str.lower), lambda w: w in {"none", "slurm", "pbs"}),

    # Provide a string with all the configuration
    Optional("free_format", default=None): Or(str, None)
    
    # Number of computing nodes to request
    Optional("nodes", default=1): int,

    # Number of CPUs per task
    Optional("cpus_per_task", default=None): Or(int, None),

    # Total time to request
    Optional("wall_time", default="01:00:00"): str,

    # Name of the partition to run
    Optional("partition_name", default=None): Or(str, None),
})

COMPUTE_SCHEMA = Schema({
    # Server URL
    "url": str,

    # Name to which the property belongs. e.g. Theory level
    "collection_name": str,

    # Command use to run the workflow
    "command": str,

    # Job scheduler
    "scheduler": SCHEMA_SCHEDULER,

    # Path to the directory where the calculations are going to run
    Optional("workdir", default="workdir_moka"): str,

    # Status of the job to query
    Optional("job_status", default="AVAILABLE"): And(
        str, lambda w: w in {"AVAILABLE", "DONE", "FAILED", "RUNNING", "RESEVERED"}),

    # Maximum number of jobs to compute
    Optional("max_jobs", default=10): int

})

QUERY_SCHEMA = Schema({
    # Server URL
    "url": str,

    # Name to which the property belongs. e.g. Theory level
    "collection_name": str,

    # Name to store the properties as csv
    Optional("output_file", default="output_properties.csv"): str
})

ADD_SCHEMA = Schema({
    # Server URL
    "url": str,

    # Settings to run the calculations
    "settings": dict,

    # Target collection to get the smiles from
    "target_collection": str,

    # Name of the new collection to store the properties
    "new_collection": str
})

REPORT_SCHEMA = Schema({
    # Server URL
    "url": str,

    # Name to which the property belongs. e.g. Theory level
    "collection_name": str,

    # Path to the csv containing the results
    "path_results": str
})

available_schemas = {"compute": COMPUTE_SCHEMA, "query": QUERY_SCHEMA, "add": ADD_SCHEMA,
                     "report": REPORT_SCHEMA}


def validate_input(file_input: Path, action: str) -> Options:
    """Check the input validation against an schema."""
    with open(file_input, 'r') as f:
        dict_input = yaml.load(f.read(), Loader=yaml.FullLoader)

    action_schema = available_schemas[action]
    try:
        data = action_schema.validate(dict_input)
        return Options(data)
    except SchemaError as err:
        msg = f"There was an error in the input yaml provided:\n{err}"
        print(msg)
        raise
