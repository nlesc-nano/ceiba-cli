"""Interface to `openstack swift <https://docs.openstack.org/swift/latest/>`_.

API
---
autofunction:: save_large_objects
"""

import json
import logging
from typing import Any, Dict, Iterable, List

from swiftclient.service import SwiftError, SwiftService

from .utils import Options

__all__ = ["save_large_objects"]

logger = logging.getLogger(__name__)


def create_swift_client():
    """Connect with the swift client."""
    # Options to authenticate
    options = {"auth_version": "1.0",
               "user": "test:tester",
               "key": "testing",
               "auth": "http://127.0.0.1:8080/auth/v1.0"}

    return SwiftService(options)


def check_action(reply: Dict[str, Any]) -> Dict[str, Any]:
    """Check that the reply contains a message of success."""
    if isinstance(reply, dict) and not reply["success"]:
        msg = json.dumps(reply, indent=4)
        raise RuntimeError(f"Error communicating with the large object storage:\n{msg}")
    return reply


def execute_swift_action(action: str, container: str, **kwargs: Dict[str, Any]) -> Any:
    """Execute a given action with the swift client."""
    # use the same collection name to store the large files
    with create_swift_client() as swift:
        function = getattr(swift, action)
        try:
            return function(container=container, **kwargs)

        except SwiftError as err:
            logger.error(err.value)


def list_container(container: str) -> List[str]:
    """List the container entry."""
    return execute_swift_action("list", container)


def save_large_objects(info: Options, prop_data: Dict[str, Any]) -> str:
    """Send the large objects specified in prop_data to the openstack swift service.

    Parameters
    ----------
    info
        to communicate with the service
    prop_data
        property data

    Returns
    -------
    str
        JSON string with the objects metadata

    """
    # Use the same collection name to store the large files
    container = prop_data["collection_name"]
    # objects to be store
    files = prop_data["large_objects"]

    # Create container if doesn't exist and store the files
    execute_swift_action("post", container)
    # Upload files
    reply = execute_swift_action("upload", container, objects=files)
    return check_action(reply)    
