"""Module to validate the user's input."""

import yaml
from pathlib import Path
from schema import Optional, Or, Schema, SchemaError
from .utils import Options


COMPUTE_SCHEMA = Schema({})
QUERY_SCHEMA = Schema({})

available_schemas = {"compute": COMPUTE_SCHEMA, "query": QUERY_SCHEMA}

def validate_input(file_input: Path, action: str) -> Options:
    """Check the input validation against an schema."""
    with open(file_input, 'r') as f:
        dict_input = yaml.load(f.read(), Loader=yaml.FullLoader)

    action_schema = available_schemas[action]
    try:
        data = action_schema.validate(dict_input)
        return Options(data)
    except SchemaError as err:
        msg = f"There was an error in the input yaml provided:\n{err}"
        print(msg)
        raise
