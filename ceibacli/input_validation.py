"""Module to validate the user's input."""

from pathlib import Path
from typing import Iterable

import yaml
from schema import And, Optional, Or, Schema, SchemaError, Use

from .utils import Options

DEFAULT_WEB = "http://insilico.quantoptic-nlesc.surf-hosted.nl:8080/graphql"


def is_in_array_uppercase(array: Iterable[str]) -> Schema:
    """Create an schema checking that the keyword matches one of the expected values."""
    return And(
        str, Use(str.upper), lambda s: s in array)


SCHEDULER_SCHEMA = Schema({
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

DEFAULTS_SCHEDULER = SCHEDULER_SCHEMA.validate({})

COMPUTE_SCHEMA = Schema({
    # Server web
    Optional("web", default=DEFAULT_WEB): str,

    # Name to which the property belongs. e.g. Theory level
    "collection_name": str,

    # Command use to run the workflow
    Optional("command", default="compute_properties"): str,

    # Job scheduler
    Optional("scheduler", default=DEFAULTS_SCHEDULER): SCHEDULER_SCHEMA,

    # Path to the directory where the calculations are going to run
    Optional("workdir", default="workdir_ceibacli"): str,

    # Status of the job to query
    Optional("job_status", default="AVAILABLE"): And(
        str, lambda w: w in {"AVAILABLE", "DONE", "FAILED", "RUNNING", "RESEVERED"}),

    # Maximum number of jobs to compute
    Optional("max_jobs", default=10): int,

    # Request either the smallest or largest available jobs
    Optional("job_size", default=None): Or(None, is_in_array_uppercase({"SMALL", "LARGE"}))
})

QUERY_SCHEMA = Schema({
    # Server web
    Optional("web", default=DEFAULT_WEB): str,

    # Name to which the property belongs. e.g. Theory level
    Optional("collection_name", default=None): Or(str, None)
})

ADD_SCHEMA = Schema({
    Optional("web", default=DEFAULT_WEB): str,

    # Path to the file with the jobs in JSON formt
    "jobs": str,

    # Name of the collection to store the properties
    "collection_name": str,
})

LARGE_OBJECTS_SCHEMA = Schema({
    # web to the datastorage service. e.g. "http://large_scientific_data_storage.pi"
    "web": str,
    # The large file(s) to search for. e.g. output*hdf5""
    "patterns": [str],
})

REPORT_SCHEMA = Schema({
    Optional("web", default=DEFAULT_WEB): str,

    # Path to the folder containing the results (default workdir_ceibacli)
    Optional("path_results", default="workdir_ceibacli"): str,

    # Pattern to search for the result files
    Optional("output", default="result*csv"): str,

    # Pattern to search for the input files used in the simulation
    Optional("input", default="inputs*json"): str,

    # The data to report is associated to a job
    Optional("has_metadata", default=True): bool,

    # If there is not metadata a collection name is required
    Optional("collection_name", default=None): Or(None, str),

    # If the data is already in server you can either:
    # KEEP the old data
    # OVERWRITE and discard the old data
    # MERGE the new and the old data
    # APPEND new data at the end of the old data array
    Optional(
        "duplication_policy", default="MERGE"): is_in_array_uppercase(
            {"KEEP", "OVERWRITE", "MERGE", "APPEND"}),

    # Metadata to store large objects
    Optional("large_objects", default=None): Or(None, LARGE_OBJECTS_SCHEMA)
})

CHANGE_POLICY_SCHEMA = Schema({
    # Old status to change
    Optional("old_status", default="RUNNING"): str,
    # New status to add
    Optional("new_status", default="AVAILABLE"): str,
    # Apply changes to all `old_status` older than specificied in hours
    Optional("expiration_time", default=168): int})

DEFAULTS_CHANGE_POLICY = CHANGE_POLICY_SCHEMA.validate({})

MANAGE_SCHEMA = Schema({
    # Name to which the property belongs
    "collection_name": str,

    # Server web
    Optional("web", default=DEFAULT_WEB): str,

    Optional("change_status", default=DEFAULTS_CHANGE_POLICY): CHANGE_POLICY_SCHEMA})

LOGIN_SCHEMA = Schema({
    # Token to authenticate
    "token": str,

    # Server web
    Optional("web", default=DEFAULT_WEB): str

})

available_schemas = {"compute": COMPUTE_SCHEMA, "query": QUERY_SCHEMA, "add": ADD_SCHEMA,
                     "report": REPORT_SCHEMA, "manage": MANAGE_SCHEMA, "login": LOGIN_SCHEMA}


def validate_input(file_input: Path, action: str) -> Options:
    """Check the input validation against an schema."""
    with open(file_input, 'r') as handler:
        dict_input = yaml.load(handler.read(), Loader=yaml.FullLoader)
    if action not in available_schemas:
        raise RuntimeError(f"unknown action: {action}\nFor more info run:``ceibacli --help``")

    action_schema = available_schemas[action]
    try:
        data = action_schema.validate(dict_input)
        return Options(data)
    except SchemaError as err:
        msg = f"There was an error in the input yaml provided:\n{err}"
        print(msg)
        raise
