"""Module to create mutations perform by the server."""

from typing import DefaultDict, Dict

__all__ = ["create_job_mutation", "create_job_status_mutation", "create_job_update_mutation",
           "create_property_mutation"]


def create_property_mutation(prop_info: Dict[str, str]) -> str:
    """Create a string with the mutation to update a property."""
    inp = f"""
  mutattion {{
    updateProperty() {{
      _id: {prop_info['smile_id']}
      collection_name: "{prop_info['collection_name']}"
      data: "{prop_info['data']}"
      geometry: "{prop_info['geometry']}"
      input: "{prop_info['input']}
    }}
  }}
"""
    return inp


def create_job_mutation(job_info: Dict[str, str], prop_info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  createJob(input: {{
    _id: {job_info['job_id']}
    property: {{
      _id: {prop_info['smile_id']}
      smile: "{prop_info['smile']}"
      collection_name: "{prop_info['collection_name']}"

    }}
    status: {job_info['status']}
    settings: "{job_info['settings']}"
  }}) {{
    _id
    status
    property {{
      _id
      smile
      collection_name
    }}
  }}
}}
"""
    return format_null(inp)


def create_job_update_mutation(job_info: DefaultDict[str, str], prop_info: DefaultDict[str, str]) -> str:
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
      geometry: "{prop_info['geometry']}"
      input: "{prop_info['input']}"

    }}
    status: {job_info['status']}
    user: "{job_info['user']}"
    platform: "{job_info['platform']}"
    report_time: {job_info['report_time']}

  }}) {{
    _id
    status
  }}
}}
"""
    return format_null(inp)


def create_job_status_mutation(info: Dict[str, str]) -> str:
    """Create string with mutation to add a new job to the server."""
    inp = f"""
    mutation {{
  updateJobStatus(input: {{
    _id: {info['job_id']}
    status: {info['status']}
    collection_name: "{info['collection_name']}"
    schedule_time: {info['schedule_time']}
    report_time: {info['report_time']}
}}) {{
    _id
    status
  }}
}}
"""
    return format_null(inp)


def format_null(string: str) -> str:
    """Remove the quotes from the null values."""
    return string.replace("\"null\"", "null")
