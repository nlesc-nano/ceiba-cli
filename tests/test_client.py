"""Module to test the communcation with the server."""

import json

from moka.client import query_server


def test_client():
    """Test the request funcionality."""
    data = json.loads(query_server('http://httpbin.org/post', "value"))

    assert data["query"] == "value"
