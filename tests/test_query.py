"""Test query functionality."""
from pathlib import Path

from pytest_mock import MockFixture

from ceibacli.actions import query_properties
from ceibacli.input_validation import validate_input
from ceibacli.utils import Options

from .utils_test import PATH_TEST, read_mocked_reply


def test_query(mocker: MockFixture, tmp_path: Path):
    """Test the functionality to update jobs."""
    # Read and Validate user input
    path_input = PATH_TEST / "input_test_query.yml"
    opts = validate_input(path_input, "query")
    opts.output_file = (tmp_path / "output.csv").absolute().as_posix()

    # Mock the server call
    mocker.patch("ceibacli.actions.query.query_server",
                 return_value=read_mocked_reply("query_mocked.json"))

    df = query_properties(opts)
    assert len(df) == 10


def test_query_collections(mocker: MockFixture):
    """Test the funcionality to query the collections."""
    opts = Options({"url": "http://localhost:8080/graphql"})
    mocker.patch("ceibacli.actions.query.query_server",
                 return_value={"collections": [
                     {"name": "foo", "size": 23}, {"name": "bar", "size": 42}]})

    df = query_properties(opts)
    assert all(name in df['name'].values for name in {'foo', 'bar'})
