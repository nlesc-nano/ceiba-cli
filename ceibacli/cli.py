"""Module to read user input and perform the requested input action."""
import argparse
import logging
import sys
import tempfile
from pathlib import Path
from typing import Tuple

import pkg_resources
import yaml

from .actions import (add_job, compute_jobs, login_insilico, manage_jobs, query_properties,
                      report_properties)
from .input_validation import DEFAULT_WEB, validate_input
from .utils import Options, exists

logger = logging.getLogger(__name__)

VERSION = pkg_resources.get_distribution('ceibacli').version


def configure_logger(workdir: Path) -> None:
    """Set the logging infrasctucture."""
    file_log = workdir / 'ceibacli_output.log'
    logging.basicConfig(filename=file_log, level=logging.INFO,
                        format='%(asctime)s  %(message)s',
                        datefmt='[%I:%M:%S]')
    handler = logging.StreamHandler()
    handler.terminator = ""

    path = pkg_resources.resource_filename('ceibacli', '')

    logger.info(f"\nUsing ceibacli version: {VERSION}\n")
    logger.info(f"ceibacli path is: {path}\n")
    logger.info(f"Working directory is: {workdir.absolute().as_posix()}\n")


def parse_user_arguments() -> Tuple[str, Options]:
    """Read the user arguments."""
    parser = argparse.ArgumentParser("ceibacli")
    parser.add_argument('--version', action='version', version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(
        help="Interact with the properties web service", dest="command")

    # Common arguments
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Common collection argument
    parent_parser.add_argument("-i", "--input", type=exists, help="Yaml input file")
    parent_parser.add_argument("-w", "--web", default=DEFAULT_WEB, help="Web Service URL")

    # Command line arguments share
    collection_parser = argparse.ArgumentParser(add_help=False)
    collection_parser.add_argument("-c", "--collection_name", help="Collection name")

    # Login into the web service
    login_parser = subparsers.add_parser("login", help="Log in to the Insilico web service")
    login_parser.add_argument("-w", "--web", default=DEFAULT_WEB, help="Web Service URL")
    login_parser.add_argument("-t", "--token", required=True, help="GitHub access Token")

    # Request new jobs to run from the database
    subparsers.add_parser("compute", help="Compute available jobs", parents=[parent_parser, collection_parser])

    # Report properties to the database
    subparsers.add_parser("report", help="Report the results back to the server", parents=[parent_parser, collection_parser])

    # Request data from the database
    subparsers.add_parser(
        "query", help="Query some properties from the database",
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
    input_file = getattr(args, "input", None)
    if input_file is None:
        user_input = {key: value for key, value in vars(args).items() if key not in {"command"}}
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
        add_job(opts)
    elif command == "manage":
        logger.info("MANAGE JOBS STATE!")
        manage_jobs(opts)
    elif command == "login":
        logger.info("LOGGING INTO THE INSILICO WEB SERVICE!")
        login_insilico(opts)


if __name__ == "__main__":
    main()
