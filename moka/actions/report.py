"""Module to move the data back to the server.

API
---
.. autofunction:: report_properties

"""

import getpass
import logging
import platform
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import yaml

from ..client import query_server
from ..client.mutations import create_job_update_mutation
from ..utils import Options

logger = logging.getLogger(__name__)


def report_properties(opts: Options) -> None:
    """Send computed properties to the server."""
    folders = collect_results(Path(opts.path_results))

    # Add metadata to the jobs
    shared_data = {
        "user": getpass.getuser(),
        "platform": platform.platform(),
        "report_time": datetime.timestamp(datetime.now())}

    # Create job object
    for path in folders:
        job_data = defaultdict(lambda: "null")
        job_data.update(shared_data)
        # Read data from result folder
        job_medata, prop_data = retrieve_data(path, opts.pattern)
        job_data.update(job_medata)
        # Send data to the web server
        query = create_job_update_mutation(job_data, prop_data)
        query_server(opts.url, query)
        logger.info(f"Properties for smile:{prop_data['smile']} have been reported!")


def retrieve_data(path: Path, pattern: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Read data and metadata from the results folder."""
    # Read metadata from results folder
    metadata = read_metadata(path)
    prop_metadata = metadata["property"]

    # Read data from results folder as pandas DataFrame
    try:
        df = read_result_from_folder(path, pattern)
        data = df.to_json()
        data = data.replace('\"', '\\"')
        status = "DONE"
    except FileNotFoundError:
        status = "FAILED"
        data = "null"

    prop_data = defaultdict(lambda: "null")
    prop_data.update({
        "smile_id": prop_metadata["smile_id"],
        "smile": prop_metadata["smile"],
        "collection_name": prop_metadata["collection_name"],
        "data": data})

    job_medata = {"job_id": metadata["job_id"], "status": status}
    return job_medata, prop_data


def collect_results(path_results: Path) -> List[Path]:
    """Gather all the results from the jobs."""
    return [x for x in path_results.glob("job_*") if x.is_dir()]


def read_result_from_folder(folder: Path, pattern: str) -> pd.DataFrame:
    """Extract the results from the output files using ``pattern``."""
    result_file = next(folder.glob(pattern), None)
    if result_file is None:
        msg = f"There is not results file: {folder}/{pattern}"
        logger.warn(msg)
        raise FileNotFoundError(msg)

    return read_properties_from_csv(result_file)


def read_properties_from_csv(path_results: Path) -> pd.DataFrame:
    """From a csv file to a pandas DataFrame."""
    df = pd.read_csv(path_results).reset_index(drop=True)

    # clean the data
    columns_to_exclude = [x for x in df.columns if x in {"smiles"}]
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.drop(columns=columns_to_exclude, inplace=True)
    return df


def read_metadata(path_job: Path) -> Dict[str, Any]:
    """Read the jobs metadata information from the job's workdir."""
    path_metadata = path_job / "metadata.yml"
    with open(path_metadata, 'r') as handler:
        return yaml.load(handler.read(), Loader=yaml.FullLoader)
