"""Check that the openstack swift interface works properly."""

import json
from pathlib import Path

import numpy as np

from moka.swift_interface import list_container, save_large_objects
from moka.utils import Options


def test_save_large_object(tmp_path: Path):
    """Check that the object are properly store."""
    # Generate some data to store
    data = np.random.normal(size=100)
    name = (tmp_path / "data").absolute().as_posix()
    path = f"{name}.npy"

    np.save(path, data)

    container = "awesome_collection"
    prop_data = {"collection_name": container,
                 "large_objects": json.dumps({name: path})}
    save_large_objects(Options(), prop_data)
    output = next(list_container(container))
    # The data has been store in the service
    assert output['success']

    # Check the path
    listing = output['listing'][0]
    path = Path(listing['name'])
    assert path.name == "data.npy"
