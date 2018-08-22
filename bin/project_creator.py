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
        self._setup_environment_file(location)
        self._modify_wsgi_file(location)
        self._modify_urls_file(location)

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

    def _setup_environment_file(self, location):
        # Rename example file
        source = os.path.join(location, "env.example")
        target = os.path.join(location, ".env")
        command = ["mv", "-f", source, target]
        self._run_command(command, False)

    def _modify_wsgi_file(self, location):
        path = os.path.join(location, "conf", "wsgi.py")

        with open(path, "r") as fh:
            contents = fh.read()

        old_string = "import os"
        new_string = "{}\nimport dotenv".format(old_string)
        contents = contents.replace(old_string, new_string)

        old_string = "from django.core.wsgi import get_wsgi_application"
        new_string = "{}\n\ndotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))".format(
            old_string)
        contents = contents.replace(old_string, new_string)

        with open(path, "w") as fh:
            fh.write(contents)

    def _modify_urls_file(self, location):
        path = os.path.join(location, "conf", "urls.py")

        with open(path, "r") as fh:
            contents = fh.read()

        # Add django imports
        new_imports = [
            "from django.conf import settings",
        ]
        old_string = "from django.urls import path"
        new_string = "{}\n{}".format(old_string, "\n".join(new_imports))
        contents = contents.replace(old_string, new_string)

        # Add imports
        new_imports = [
            "import allauth",
            "import dynamic_raw_id",
        ]
        old_string = "from django.conf import settings"
        new_string = "{}\n\n{}".format(old_string, "\n".join(new_imports))
        contents = contents.replace(old_string, new_string)

        # Add patterns
        new_patterns = [
            "    path('accounts/', allauth.urls),",
            "    path('admin/dynamic_raw_id/', dynamic_raw_id.urls),",
        ]
        old_string = "    path('admin/', admin.site.urls),"
        new_string = "{}\n\n{}".format(old_string, "\n".join(new_patterns))
        contents = contents.replace(old_string, new_string)

        # Add media access if DEBUG
        contents += "\n"
        contents += "if settings.DEBUG:\n"
        contents += "    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"

        # Add admin titles
        contents += "\n\n"
        contents += "admin.site.site_header = 'Base Project'\n"
        contents += "admin.site.index_header = 'Base Project'"

        with open(path, "w") as fh:
            fh.write(contents)


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
