#!/usr/bin/env python

import argparse
import logging
import os
import sys

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s",
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Creates a Django Project")
    parser.add_argument('location', help='Location for the new project, this must not exist.')

    args = parser.parse_args(sys.argv[1:])
    if os.path.exists(args.location):
        raise Exception("The location already exists")


if __name__ == "__main__":
    main()
