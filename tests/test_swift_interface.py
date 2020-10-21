"""Check that the openstack swift interface works properly."""

from pathlib import Path
import numpy as np
from moka.swift_interface import list_container, save_large_objects
from moka.utils import Options


def test_save_large_object(tmp_path: Path):
    """Check that the object are properly store."""
    # Generate some data to store
    data = np.random.normal(size=100)
    path = (tmp_path / "data").absolute().as_posix()
    np.save(path, data)

    container = "awesome_collection"
    prop_data = {"collection_name": container,
                 "large_objects": [f"{path}.npy"]}
    output = save_large_objects(Options(), prop_data)
    print(next(output))
    assert False
    # output = list_container(container)
    # print(output)
    # # listing = output["listing"][0]
    # # print(listing)
    # assert path == listing["name"]
