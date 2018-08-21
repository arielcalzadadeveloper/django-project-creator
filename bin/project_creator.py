#!/usr/bin/env python

import argparse
import logging
import os
import subprocess
import sys

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s",
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def run_command(command):
    """Run command using subprocess module."""
    try:
        logger.debug("Running: {}".format(command))
        command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process_output, _ = command_line_process.communicate()

        if command_line_process.returncode != 0:
            raise Exception(process_output)
    except Exception as e:
        raise Exception(e)


def main():
    parser = argparse.ArgumentParser(description="Creates a Django Project")
    parser.add_argument('location', help='Location for the new project, this must not exist.')

    args = parser.parse_args(sys.argv[1:])
    if os.path.exists(args.location):
        raise Exception("The location already exists")

    command = [
        "django-admin",
        "startproject",
        "conf",
        args.location
    ]
    run_command(command)


if __name__ == "__main__":
    main()
