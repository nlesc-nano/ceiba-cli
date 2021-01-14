"""Utility functions."""

import json
from typing import Any, Dict, List, TypeVar
import pandas as pd

T = TypeVar('T')


class Options(dict):
    """Extend the base class dictionary with a '.' notation.
    
    example:
    .. code-block:: python
       d = Options({'a': 1})
       d['a'] # 1
       d.a    # 1
       d.b = 3
       d["b"] == 3  # True
    """

    def __init__(self, *args, **kwargs):
        """ Create a recursive Options object"""
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = Options(v)

    def __getattr__(self, attr):
        """ Allow `obj.key` notation"""
        return self.get(attr)

    def __setattr__(self, key, value):
        """ Allow `obj.key = new_value` notation"""
        self.__setitem__(key, value)

    def to_dict(self) -> Dict[str, T]:
        """Convert to a normal dictionary."""
        def converter(var):
            return var.to_dict() if isinstance(var, Options) else var

        return {k: converter(v) for k, v in self.items()}


def json_properties_to_dataframe(properties: List[Dict[str, Any]]) -> pd.DataFrame:
    """Transform a JSON list of dictionaries into a pandas DataFrame."""
    df = pd.DataFrame(properties)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if 'data' in df.columns:
        df['data'].fillna("{}", inplace=True)
        df['data'] = df['data'].apply(lambda x: json.loads(x))

    return df
