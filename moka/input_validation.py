"""Module to validate the user's input."""

from pathlib import Path
from typing import Iterable

import yaml
from schema import And, Optional, Or, Schema, SchemaError, Use

from .utils import Options


def is_in_array_uppercase(array: Iterable[str]) -> Schema:
    """Create an schema checking that the keyword matches one of the expected values."""
    return And(
        str, Use(str.upper), lambda s: s in array)


SCHEMA_SCHEDULER = Schema({
    Optional("name", default="none"): And(
        str, Use(str.lower), lambda w: w in {"none", "slurm"}),

    # Provide a string with all the configuration
    Optional("free_format", default=None): Or(str, None),

    # Number of computing nodes to request
    Optional("nodes", default=1): int,

    # Number of CPUs per task
    Optional("cpus_per_task", default=None): Or(int, None),

    # Total time to request
    Optional("wall_time", default="01:00:00"): str,

    # Name of the partition to run
    Optional("partition_name", default=None): Or(str, None),
})

DEFAULTS_SCHEDULER = SCHEMA_SCHEDULER.validate({})

COMPUTE_SCHEMA = Schema({
    # Server URL
    "url": str,

    # Name to which the property belongs. e.g. Theory level
    "collection_name": str,

    # Command use to run the workflow
    "command": str,

    # Job scheduler
    Optional("scheduler", default=DEFAULTS_SCHEDULER): SCHEMA_SCHEDULER,

    # Path to the directory where the calculations are going to run
    Optional("workdir", default="workdir_moka"): str,

    # Status of the job to query
    Optional("job_status", default="AVAILABLE"): And(
        str, lambda w: w in {"AVAILABLE", "DONE", "FAILED", "RUNNING", "RESEVERED"}),

    # Maximum number of jobs to compute
    Optional("max_jobs", default=10): int,

    # Request either the smallest or largest available jobs
    Optional("job_size", default=None): Or(None, is_in_array_uppercase({"SMALL", "LARGE"}))
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

    # Path to the folder containing the results (default workdir_moka)
    "path_results": str,

    # Pattern to search for the result files
    Optional("pattern", default="result*csv"): str,

    # The data to report is not associated to a job
    Optional("is_standalone", default=False): bool,

    # If the data is already in server you can either:
    # KEEP the old data
    # OVERWRITE and discard the old data
    # MERGE the new and the old data
    # APPEND new data at the end of the old data array
    Optional(
        "duplication_policy", default="KEEP"): is_in_array_uppercase(
            {"KEEP", "OVERWRITE", "MERGE", "APPEND"})

})

available_schemas = {"compute": COMPUTE_SCHEMA, "query": QUERY_SCHEMA, "add": ADD_SCHEMA,
                     "report": REPORT_SCHEMA}


def validate_input(file_input: Path, action: str) -> Options:
    """Check the input validation against an schema."""
    with open(file_input, 'r') as handler:
        dict_input = yaml.load(handler.read(), Loader=yaml.FullLoader)

    if action not in available_schemas:
        raise RuntimeError(f"unknown action: {action}\nFor more info run:``moka --help``")

    action_schema = available_schemas[action]
    try:
        data = action_schema.validate(dict_input)
        return Options(data)
    except SchemaError as err:
        msg = f"There was an error in the input yaml provided:\n{err}"
        print(msg)
        raise
