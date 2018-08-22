#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
import uuid


class ProjectCreator:
    BASE_PROJECT_URL = "https://github.com/arielcalzadadeveloper/django-base-project.git"

    def create(self, location):
        self._create_project(location)
        self._get_base_project(location)

    @staticmethod
    def _run_command(command, with_subprocess=True):
        """Run shell command"""
        print("Running command: {}".format(" ".join(command)))

        if with_subprocess:
            try:
                command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                process_output, _ = command_line_process.communicate()

                if command_line_process.returncode != 0:
                    raise Exception(process_output)
            except Exception as e:
                raise Exception(e)
        else:
            os.system(" ".join(command))

    def _create_project(self, location):
        command = [
            "django-admin",
            "startproject",
            "conf",
            location
        ]

        self._run_command(command)

    def _get_base_project(self, location):
        temporal_location = os.path.join(location, uuid.uuid4().hex)

        command = [
            "git",
            "clone",
            self.BASE_PROJECT_URL,
            temporal_location
        ]

        self._run_command(command)

        command = [
            "mv",
            "-f",
            "{}/*".format(temporal_location),
            location
        ]

        self._run_command(command, False)

        for file_name in [".yarnrc", ".gitignore"]:
            command = [
                "mv",
                "-f",
                os.path.join(temporal_location, file_name),
                location
            ]

        self._run_command(command, False)

        shutil.rmtree(temporal_location)


def main():
    parser = argparse.ArgumentParser(description="Creates a Django Project")
    parser.add_argument('location', help='Location for the new project, this must not exist.')

    args = parser.parse_args(sys.argv[1:])
    if not os.path.exists(args.location):
        os.makedirs(args.location)

    creator = ProjectCreator()
    creator.create(args.location)


if __name__ == "__main__":
    main()
