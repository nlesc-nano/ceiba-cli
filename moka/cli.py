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
from .input_validation import validate_input
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

    # Request new jobs to run from the database
    parser_jobs = subparsers.add_parser("compute", help="compute available jobs")
    parser_jobs.add_argument("-i", "--input", type=exists, help="Yaml input file")

    # Report properties to the database
    parser_report = subparsers.add_parser("report", help="Report the results back to the server")
    parser_report.add_argument("-i", "--input", type=exists, help="Yaml input file")

    # Request data from the database
    parser_query = subparsers.add_parser("query", help="query some properties from the database")
    parser_query.add_argument("-i", "--input", type=exists, help="Yaml input file")

    # Add new Job to the database
    parser_add = subparsers.add_parser("add", help="Add new jobs to the database")
    parser_add.add_argument("-i", "--input", type=exists, help="Yaml input file")

    # Manage the Jobs status
    parser_add = subparsers.add_parser("manage", help="Change jobs status")
    parser_add.add_argument("-i", "--input", type=exists, help="Yaml input file")
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit()

    return args.command, handle_input(args)


def handle_input(args: argparse.Namespace) -> Options:
    """Check user input."""
    if args.input is not None:
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
