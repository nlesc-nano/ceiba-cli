"""Module to read user input and perform the requested input action."""
import logging
import argparse

logger = logging.getLogger(__name__)


def main():
    """Parse the command line arguments to screen smiles."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="compute or query some molecular properties")

    # Request new jobs to run from the database
    parser_jobs = subparsers.add_parser("compute", help="compute available jobs")
    parser_jobs.add_argument('-m', '--max', type=int, help="Maximum number of jobs to run", default=10)

    # Request data from the database
    parser_query = subparsers.add_parser("query", help="query some properties from the database")
    parser_query.add_argument('-i', required=True, help="Input file with options")

    args = parser.parse_args()

    if getattr(args, 'i', None) is not None:
        print("querying molecular properties!")
    else:
        print("computing properties")


if __name__ == "__main__":
    main()