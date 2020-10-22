"""Check that the openstack swift interface works properly."""

import json
from pathlib import Path

import numpy as np

from moka.swift_interface import SwiftAction


def test_save_large_object(tmp_path: Path):
    """Check that the object are properly store."""
    # Generate some data to store
    data = np.random.normal(size=100)
    name = (tmp_path / "data").absolute().as_posix()
    path_str = f"{name}.npy"

    np.save(path_str, data)

    container = "awesome_collection"
    prop_data = {"collection_name": container,
                 "large_objects": json.dumps({name: path_str})}
    swift = SwiftAction("https://awesome_scientific_data.pi")
    swift.upload(prop_data)
    output = next(swift.list_container(container))
    # # The data has been store in the service
    assert output['success']

    # Check the path
    listing = output['listing'][0]
    path = Path(listing['name'])
    assert path.name == "data.npy"

    # Remove the data from the storage
    swift.delete(container, objects=[path_str[1:]])
    # Check that there are no objects in the container
    data = list(swift.list_container(container))
    assert not data
