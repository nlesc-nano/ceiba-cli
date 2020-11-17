"""Module to read user input and perform the requested input action."""
import argparse
import logging
import sys
import tempfile
from pathlib import Path
from typing import Tuple

import pkg_resources
import yaml

from .actions import (add_jobs, compute_jobs, manage_jobs, query_properties,
                      report_properties)
from .input_validation import DEFAULT_URL, validate_input
from .utils import Options

logger = logging.getLogger(__name__)

VERSION = pkg_resources.get_distribution('moka').version


def exists(input_file: str) -> Path:
    """Check if the input file exists."""
    path = Path(input_file)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{input_file} doesn't exist!")

    return path


def configure_logger(workdir: Path) -> None:
    """Set the logging infrasctucture."""
    file_log = workdir / 'moka_output.log'
    logging.basicConfig(filename=file_log, level=logging.INFO,
                        format='%(asctime)s  %(message)s',
                        datefmt='[%I:%M:%S]')
    handler = logging.StreamHandler()
    handler.terminator = ""

    path = pkg_resources.resource_filename('moka', '')

    logger.info(f"\nUsing moka version: {VERSION}\n")
    logger.info(f"moka path is: {path}\n")
    logger.info(f"Working directory is: {workdir.absolute().as_posix()}\n")


def parse_user_arguments() -> Tuple[str, Options]:
    """Read the user arguments."""
    parser = argparse.ArgumentParser("moka")
    parser.add_argument('--version', action='version', version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(
        help="Interact with the properties web service", dest="command")

    # Common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    # you should provide either the input file with the arguments
    # or each argument in the command line
    group = parent_parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--input", type=exists, help="Yaml input file")
    group.add_argument("-u", "--url", default=DEFAULT_URL, help="Web Service URL")

    # Common collection argument
    collection_parser = argparse.ArgumentParser(add_help=False)
    collection_parser.add_argument("--collection_name", help="Collection name")

    # Request new jobs to run from the database
    subparsers.add_parser("compute", help="compute available jobs", parents=[parent_parser])

    # Report properties to the database
    subparsers.add_parser(
        "report", help="Report the results back to the server", parents=[parent_parser])

    # Request data from the database
    subparsers.add_parser(
        "query", help="query some properties from the database",
        parents=[parent_parser, collection_parser])

    # Add new Job to the database
    subparsers.add_parser(
        "add", help="Add new jobs to the database", parents=[parent_parser])

    # Manage the Jobs status
    subparsers.add_parser(
        "manage", help="Change jobs status", parents=[parent_parser, collection_parser])

    # Read the arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit()

    return args.command, handle_input(args)


def handle_input(args: argparse.Namespace) -> Options:
    """Check user input."""
    if getattr(args, "input", None) is not None:
        input_file = args.input
    else:
        user_input = {key: value for key, value in vars(args).items() if key not in {"command", "input"}}
        input_file = Path(tempfile.gettempdir()) / "user_input.yml"
        with open(input_file, 'w') as handler:
            yaml.dump(user_input, handler)

    return validate_input(input_file, action=args.command)


def main():
    """Parse the command line arguments to compute or query data from the database."""
    command, opts = parse_user_arguments()

    # Initialize logger
    configure_logger(Path("."))

    if command == "query":
        logger.info("QUERYING MOLECULAR PROPERTIES!")
        query_properties(opts)
    elif command == "compute":
        logger.info("COMPUTING PROPERTIES!")
        compute_jobs(opts)
    elif command == "report":
        logger.info("REPORTING RESULTS BACK TO THE SERVER!")
        report_properties(opts)
    elif command == "add":
        logger.info("ADDING NEW JOBS TO THE DATABASE")
        add_jobs(opts)
    elif command == "manage":
        logger.info("MANAGE JOBS STATE!")
        manage_jobs(opts)


if __name__ == "__main__":
    main()
