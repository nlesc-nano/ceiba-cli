"""Check that the openstack swift interface works properly."""

import json
from pathlib import Path

import numpy as np

from moka.swift_interface import SwiftAction, check_action


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
    swift = SwiftAction("https://awesome_scientific_data.pi")
    reply = [check_action(x) for x in swift.save_large_objects(prop_data)]
    print(reply)
    output = next(swift.list_container(container))
    # # The data has been store in the service
    assert output['success']

    # Check the path
    listing = output['listing'][0]
    path = Path(listing['name'])
    assert path.name == "data.npy"
