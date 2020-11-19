"""Module to test the communcation with the server."""

import json

import pytest
from pytest_mock import MockerFixture

from moka.client import check_github_username, query_server
from moka.utils import Options


def test_client():
    """Test the request funcionality."""
    data = json.loads(query_server('http://httpbin.org/post', "value"))

    assert data["query"] == "value"


def test_client_405():
    """Check that the client recieve a 405 error when making a wrong request."""
    url = "https://data.rcsb.org/rest/v1/core/pubmed/4ACQ"

    with pytest.raises(RuntimeError) as info:
        query_server(url, "")

    error = info.value.args[0]
    assert "Error 405" in error


def test_client_error(mocker: MockerFixture):
    """Check that an error is raise if the reply contains some errors."""
    reply = Options(
        {"status_code": 200, "text": '{"errors": "Something went wrong!"}'})
    mocker.patch("requests.post", return_value=reply)

    with pytest.raises(RuntimeError) as info:
        query_server("https://awesomeness.org", "")

    error = info.value.args[0]
    assert "Something went wrong!" in error


def test_github_user():
    """Check that None is return if an invalid toke is provided."""
    username = check_github_username("invalidtoken123")
    assert username is None


def test_correct_token(mocker: MockerFixture):
    """Check that a username is returns if a valid token is provided."""
    mocked_reply = Options(
        {"status_code": 200, "text": '{"data": {"viewer": {"login": "felipeZ"}}}'})
    mocker.patch("requests.post", return_value=mocked_reply)
    username = check_github_username("validtoken")

    assert username == "felipez"
