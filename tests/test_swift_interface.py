"""Check that the openstack swift interface works properly."""

from pathlib import Path
from typing import Tuple

import numpy as np

from moka.swift_interface import SwiftAction

CONTAINER = "awesome_collection"


def save_numpy_data(tmp_path: Path) -> Tuple[str, str]:
    """Create a toy numerical array."""
    data = np.random.normal(size=100)
    name = (tmp_path / "data").absolute().as_posix()
    path_str = f"{name}.npy"
    np.save(path_str, data)

    return name, path_str


def remove_data(swift: SwiftAction, path_str: str) -> None:
    """Remove the data from the storage."""
    swift.delete(CONTAINER, objects=[path_str[1:]])
    # Check that there are no objects in the container
    data = list(swift.list_container(CONTAINER))
    assert not data


def test_save_large_object(tmp_path: Path):
    """Check that the object are properly store."""
    name, path_str = save_numpy_data(tmp_path)

    prop_data = {"collection_name": CONTAINER,
                 "large_objects": {name: path_str}}
    swift = SwiftAction()
    swift.upload(prop_data)
    output = next(swift.list_container(CONTAINER))
    # # The data has been store in the service
    assert output['success']

    # Check the path
    listing = output['listing'][0]
    path = Path(listing['name'])
    assert path.name == "data.npy"

    # Remove the data from the storage
    remove_data(swift, path_str)


def test_download(tmp_path: Path):
    """Check that the object are properly store."""
    name, path_str = save_numpy_data(tmp_path)

    # store the toy data
    prop_data = {"collection_name": CONTAINER,
                 "large_objects": {name: path_str}}
    swift = SwiftAction("https://awesome_scientific_data.pi")
    swift.upload(prop_data)

    # the file is stored without the / root slash
    path_in_storage = path_str[1:]

    # Download the data
    output = swift.download(
        CONTAINER, [path_in_storage], options={"out_directory": tmp_path.as_posix()})

    assert output[0]["success"]

    # Remove the data from the storage
    remove_data(swift, path_str)
