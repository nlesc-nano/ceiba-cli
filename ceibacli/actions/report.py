"""Module to move the data back to the server.

API
---
.. autofunction:: report_properties

"""

import getpass
import json
import logging
import platform
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, DefaultDict, Dict, List, Tuple

import pandas as pd
import yaml

from ..authentication import fetch_cookie
from ..client import query_server
from ..client.mutations import (create_job_update_mutation,
                                create_property_mutation)
from ..swift_interface import SwiftAction
from ..utils import Options, generate_smile_identifier

__all__ = ["report_properties"]

logger = logging.getLogger(__name__)


def report_properties(opts: Options) -> None:
    """Send computed properties to the server."""
    # fetch authentication credentials
    opts.cookie = fetch_cookie()

    if opts.has_metadata:
        report_jobs_properties(opts)
    elif opts.collection_name is None:
        msg = "A collection name is required if the results don't have metadata"
        raise RuntimeError(msg)
    else:
        # The results don't have  associated jobs
        report_standalone_properties(opts)


def report_standalone_properties(opts: Options) -> None:
    """Send standalone data to a given collection."""
    for output in Path(opts.path_results).glob(opts.output):
        smile, data = read_properties_from_csv(output)
        data = data.replace('\"', '\\"')
        query = create_standalone_mutation(opts, smile, data)
        query_server(opts.web, query)

    logger.info(f"Standalone data has been sent to collection: {opts.collection_name}")


def report_jobs_properties(opts: Options) -> None:
    """Report properties coming from a server's job."""
    path = Path(opts.path_results)
    if not path.exists():
        raise FileNotFoundError(f"There are not results folders:{path}")
    # Collect results folders
    folders = collect_results(path, pattern="job_*")

    # Add metadata to the jobs
    shared_data = {
        "user": getpass.getuser(),
        "platform": platform.platform(),
        "report_time": datetime.timestamp(datetime.now())}

    # Create job object
    for path in folders:
        store_single_job_data(path, opts, shared_data)


def store_single_job_data(path: Path, opts: Options, shared_data: Dict[str, Any]) -> None:
    """Retrieve and store the data for a single job."""
    job_data = defaultdict(lambda: "null")  # type: DefaultDict[str, str]
    job_data.update(shared_data)
    # Read data from result folder
    job_medata, prop_data = retrieve_data(path, opts)
    job_data.update(job_medata)
    # Store large objects using the files metadata
    if opts.large_objects is not None:
        swift = SwiftAction(opts.large_objects.web)
        job_data["large_object"] = swift.upload(prop_data)
    # Send data to the web server
    query = create_job_update_mutation(job_data, prop_data, opts)
    reply = query_server(opts.web, query)
    logger.info(reply['updateJob']['text'])


def retrieve_data(path: Path, opts: Options) -> Tuple[Dict[str, Any], DefaultDict[str, Any]]:
    """Read data and metadata from the results folder."""
    # Read metadata from results folder
    metadata = read_metadata(path)
    prop_metadata = metadata["property"]

    # Read data from results folder as pandas DataFrame
    data, status = read_data_and_job_status(path, opts.output)

    # Check if large objects need to be store
    large_objects = "null" if opts.large_objects is None else search_for_large_objects(
        path, opts.large_objects)

    prop_data = defaultdict(lambda: "null")  # type: DefaultDict[str, Any]
    prop_data.update({
        "smile_id": prop_metadata["smile_id"],
        "smile": prop_metadata["smile"],
        "collection_name": prop_metadata["collection_name"],
        "data": data,
        "large_objects": large_objects,
        "input": read_input_files(path, opts.input),
        "geometry": read_optimized_geometry(path, opts.geometry)}
    )

    job_medata = {"job_id": metadata["job_id"], "status": status}
    return job_medata, prop_data


def read_optimized_geometry(path: Path, pattern: str) -> str:
    """Retrieve the optimized geometry."""
    file_geometry = next(path.glob(pattern), None)
    if file_geometry is None:
        return "null"

    with open(file_geometry, 'r') as handler:
        geometry = handler.read()

    return json.dumps(geometry)


def read_input_files(path: Path, pattern: str) -> str:
    """Read the input files used for the simulations."""
    result_file = next(path.glob(pattern), None)
    if result_file is None:
        return "null"

    data = read_properties_from_json(result_file)
    return data.replace('\"', '\\"')


def read_data_and_job_status(path: Path, pattern: str) -> Tuple[str, str]:
    """Retrieve data and status from the job folder."""
    try:
        data = read_result_from_folder(path, pattern)
        status = "DONE"
    except FileNotFoundError:
        status = "FAILED"
        data = "null"

    return data, status


def collect_results(path_results: Path, pattern: str) -> List[Path]:
    """Gather all the results from the jobs."""
    return [x for x in path_results.glob(pattern) if x.is_dir()]


def read_result_from_folder(folder: Path, pattern: str) -> pd.DataFrame:
    """Extract the results from the output files using ``pattern``."""
    result_file = next(folder.glob(pattern), None)
    if result_file is None:
        msg = f"There is not results file: {folder}/{pattern}"
        logger.warn(msg)
        raise FileNotFoundError(msg)

    # Read the results from the file
    suffix = result_file.suffix
    if suffix == ".csv":
        _smile, data = read_properties_from_csv(result_file)
    elif suffix == ".json":
        data = read_properties_from_json(result_file)
    else:
        msg = f"There is no parser for {suffix} file format!"
        raise NotImplementedError(msg)

    return data.replace('\"', '\\"')


def read_properties_from_json(path_results: Path) -> str:
    """Read JSON file."""
    with open(path_results, 'r') as handler:
        data = json.load(handler)
    return json.dumps(data)


def read_properties_from_csv(path_results: Path) -> Tuple[str, str]:
    """From a csv file to a pandas DataFrame."""
    df = pd.read_csv(path_results).reset_index(drop=True)
    smile, = df["smiles"]
    # clean the data
    columns_to_exclude = [x for x in df.columns if x in {"smiles"}]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.drop(columns=columns_to_exclude, inplace=True)
    return smile, df.to_json()


def read_metadata(path_job: Path) -> Dict[str, Any]:
    """Read the jobs metadata information from the job's workdir."""
    path_metadata = path_job / "metadata.yml"
    if not path_metadata.exists():
        msg = f"There is no file with metadata: {path_metadata}"
        raise FileNotFoundError(msg)
    with open(path_metadata, 'r') as handler:
        return yaml.load(handler.read(), Loader=yaml.FullLoader)


def create_standalone_mutation(opts: Options, smile: str, data: str) -> str:
    """Create query to mutate standalone data."""
    info = defaultdict(lambda: "null")
    info['data'] = data

    # Read metadata from workdir
    info["smile_id"] = generate_smile_identifier(smile)
    info["smile"] = smile
    info['collection_name'] = opts.collection_name

    return create_property_mutation(opts.cookie, info)


def search_for_large_objects(path: Path, info: Options) -> Dict[str, str]:
    """Look out for output files to store using the openstack swift interface."""
    data = {}
    for pat in info.patterns:
        files = (path.glob(f"**/{pat}"))
        data.update({p.name: p.absolute().as_posix() for p in files})

    return data
