"""Test the login functionality."""
import os
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from moka.actions import login_insilico
from moka.utils import Options


def test_invalid_token(mocker: MockFixture):
    """Check that an error is raise if an invalid token is provided."""
    opts = Options({"token": "InvalidToken", "web": "localhost:8080/graphql"})

    mocker.patch("moka.actions.login.query_server", return_value={
        "authenticateUser": {"text": "Invalid token!", "status": "FAILED"}})

    with pytest.raises(RuntimeError) as info:
        login_insilico(opts)

    error = info.value.args[0]
    assert "Invalid token" in error


def test_valid_token(mocker: MockFixture):
    """Check that the authentication succeeds if a valid token is provided."""
    opts = Options({"token": "InvalidToken", "web": "localhost:8080/graphql"})

    reply_token = "InsilicoReplyToken"
    mocker.patch("moka.actions.login.query_server", return_value={
        "authenticateUser": {"text": reply_token, "status": "DONE"}})

    # File where the server reply is stored
    path_cookie = Path.home() / ".insilicoserver"
    try:
        login_insilico(opts)
        # Check that the cookie is written
        with open(path_cookie, 'r') as handler:
            reply = handler.read()
        assert reply == reply_token
    finally:
        if path_cookie.exists():
            os.remove(path_cookie)
