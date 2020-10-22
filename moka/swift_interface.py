"""Interface to `openstack swift <https://docs.openstack.org/swift/latest/>`_.

API
---
autoclass:: SwiftAction
autofunction:: check_action

"""

import json
import logging
from typing import Any, Dict, Iterable, List, Optional

from swiftclient.service import SwiftError, SwiftService


__all__ = ["SwiftAction"]

logger = logging.getLogger(__name__)


class SwiftAction:
    """Object to handle the interaction with the swift client."""

    def __init__(self, url: str):
        """Start the class using the provided url."""
        self.options = {
            "auth_version": "1.0",
            "user": "test:tester",
            "key": "testing",
            "auth": "http://127.0.0.1:8080/auth/v1.0"}

        self.swift = SwiftService(self.options)

    def execute_swift_action(self, action: str, container: str, **kwargs: Optional[Any]) -> Any:
        """Execute a given action with the swift client."""
        function = getattr(self.swift, action)
        try:
            return function(container=container, **kwargs)

        except SwiftError as err:
            logger.error(err.value)
            return None

    def list_container(self, container: str) -> Iterable[str]:
        """List the container entry."""
        return self.execute_swift_action("list", container)

    def upload(self, prop_data: Dict[str, Any], options: Optional[Dict[str, Any]] = None) -> str:
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

        # Create container if doesn't exist and store the files and
        # use the same collection name to store the large files
        check_action(self.execute_swift_action("post", container))

        # Upload and check that it works
        for reply in self.execute_swift_action(
                "upload", container, objects=files.values(), options=options):
            check_action(reply)

        # Remove the root / from the path
        return json.dumps({name: path[1:] for name, path in files.items()})

    def delete(self, container: str, objects: Optional[List[str]] = None,
               options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Remove objects or container."""
        return [check_action(x) for x in self.execute_swift_action(
            "delete", container, objects=objects, options=options)]


def check_action(reply: Dict[str, Any]) -> Dict[str, Any]:
    """Check that the reply contains a message of success."""
    if not reply["success"]:
        msg = json.dumps(reply, indent=4)
        raise RuntimeError(f"Error communicating with the large object storage:\n{msg}")
    return reply
