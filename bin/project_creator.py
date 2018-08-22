#!/usr/bin/env python

import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import uuid

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s",
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG if os.getenv("DJANGO_PROJECT_CREATOR_DEBUG", "False") == "True" else logging.INFO)

logger = logging.getLogger(__name__)


class ProjectCreator:
    BASE_PROJECT_URL = "https://github.com/arielcalzadadeveloper/django-base-project.git"

    def create(self, location):
        self._create_project(location)
        self._get_base_project(location)

    @staticmethod
    def _run_command(command):
        """Run command using subprocess module."""
        try:
            logger.debug("Running: {}".format(command))
            command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process_output, _ = command_line_process.communicate()

            if command_line_process.returncode != 0:
                raise Exception(process_output)
        except Exception as e:
            raise Exception(e)

    def _create_project(self, location):
        command = [
            "django-admin",
            "startproject",
            "conf",
            location
        ]

        self._run_command(command)

    def _get_base_project(self, location):
        logger.info("Cloning base project")
        # temporal_location = os.path.join(location, uuid.uuid4().hex)

        command = [
            "git",
            "clone",
            self.BASE_PROJECT_URL,
            location
        ]

        self._run_command(command)

        # shutil.copytree(temporal_location, location)
        # shutil.rmtree(temporal_directory)


def main():
    parser = argparse.ArgumentParser(description="Creates a Django Project")
    parser.add_argument('location', help='Location for the new project, this must not exist.')

    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.location):
        os.makedirs(args.location)

    logger.info("Creating project...")

    creator = ProjectCreator()
    creator.create(args.location)


if __name__ == "__main__":
    main()
