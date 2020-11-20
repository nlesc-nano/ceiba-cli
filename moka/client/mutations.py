"""Module to create mutations perform by the server."""

from typing import Any, DefaultDict, Dict

__all__ = ["create_job_mutation", "create_job_status_mutation", "create_job_update_mutation",
           "create_property_mutation"]


def create_property_mutation(prop_info: Dict[str, str]) -> str:
    """Create a string with the mutation to update a property."""
    inp = f"""mutation {{
    updateProperty(input: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"
      data: "{prop_info['data']}"
      geometry: "{prop_info['geometry']}"
      input: "{prop_info['input']}"
    }}) {{
    status
    text
  }}
}}
"""
    return format_null(inp)


def create_job_mutation(cookie: str, job_info: Dict[str, str], prop_info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  createJob(cookie: "{cookie}",
    input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"
    }}
    status: {job_info['status']}
    settings: "{job_info['settings']}"
  }}) {{
    status
    text
  }}
}}
"""
    return format_null(inp)


def create_job_update_mutation(
        job_info: DefaultDict[str, str], prop_info: DefaultDict[str, str],
        duplication_policy: str) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJob(input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"
      data: "{prop_info['data']}"
      geometry: {prop_info['geometry']}
      input: "{prop_info['input']}"
      large_objects: "{prop_info['large_objects']}"

    }}
    status: {job_info['status']}
    user: "{job_info['user']}"
    platform: "{job_info['platform']}"
    report_time: {job_info['report_time']}

  }},
    duplication_policy: {duplication_policy}
  ) {{
    text
    status
  }}
}}
"""
    return format_null(inp)


def create_job_status_mutation(info: Dict[str, Any]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJobStatus(input: {{
    _id: {info['job_id']}
    status: {info['status']}
    collection_name: "{info['collection_name']}"
    user: "{info['user']}"
    schedule_time: {info['schedule_time']}
    report_time: {info['report_time']}
}}) {{
    text
    status
  }}
}}
"""
    return format_null(inp)


def create_authentication_mutation(token: str) -> str:
    """Create a string representing a mutation to authenticate an user."""
    return f"""
    mutation {{
  authenticateUser(token: "{token}")
  {{
    text
    status
  }}
}}
"""


def format_null(string: str) -> str:
    """Remove the quotes from the null values."""
    return string.replace("\"null\"", "null")
