"""Module to read user input and perform the requested input action."""
import argparse
import logging
import sys
from pathlib import Path

from .actions import (add_jobs, compute_jobs, query_properties,
                      report_properties)
from .input_validation import validate_input

logger = logging.getLogger(__name__)


def exists(input_file: str) -> Path:
    """Check if the input file exists."""
    path = Path(input_file)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{input_file} doesn't exist!")

    return path


def main():
    """Parse the command line arguments to compute or query data from the database."""
    parser = argparse.ArgumentParser("moka")
    subparsers = parser.add_subparsers(help="Interact with the properties web service", dest="command")

    # Request new jobs to run from the database
    parser_jobs = subparsers.add_parser("compute", help="compute available jobs")
    parser_jobs.add_argument("input", type=exists, help="Yaml input file")

    # Report properties to the databae
    parser_report = subparsers.add_parser("report", help="Report the results back to the server")
    parser_report.add_argument("input", type=exists, help="Yaml input file")

    # Request data from the database
    parser_query = subparsers.add_parser("query", help="query some properties from the database")
    parser_query.add_argument("input", type=exists, help="Yaml input file")

    # Add new Job to the database
    parser_add = subparsers.add_parser("add", help="Add new jobs to the database")
    parser_add.add_argument("input", type=exists, help="Yaml input file")
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit()

    opts = validate_input(args.input, action=args.command)
    # opts = validate_input()
    if args.command == "query":
        print("querying molecular properties!")
        query_properties(opts)
    elif args.command == "compute":
        print("computing properties")
        compute_jobs(opts)
    elif args.command == "report":
        print("report results back to the server")
        report_properties(opts)
    elif args.command == "add":
        print("adding new jobs to the database")
        add_jobs(opts)


if __name__ == "__main__":
    main()
