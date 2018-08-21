import logging
import os
import shutil
import subprocess
import tempfile
import uuid
import unittest

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s",
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class TestProjectCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporal_directory = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.temporal_directory):
            shutil.rmtree(cls.temporal_directory)

    def _run_command(self, command):
        """Run command using subprocess module."""
        try:
            logger.debug("Running: {}".format(command))
            command_line_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process_output, _ = command_line_process.communicate()

            if command_line_process.returncode != 0:
                raise Exception(process_output)
        except Exception as e:
            raise Exception(e)

    def _create_virtualenv(self):
        """Create random virtualenv."""
        name = uuid.uuid4().hex
        path = os.path.join(self.temporal_directory, name)
        command = ["virtualenv", path]
        self._run_command(command)

        return path

    def _install_package(self, path):
        python_executable = os.path.join(path, "bin", "python")
        pip_executable = os.path.join(path, "bin", "pip")
        command = [pip_executable, "install", "git+https://github.com/arielcalzadadeveloper/django-project-creator.git"]
        self._run_command(command)

    def test_no_location(self):
        """No location provided."""
        pass

    def test_invalid_location(self):
        """Invalid location."""
        pass

    def test_valid_location(self):
        """Valid location."""
        path = self._create_virtualenv()
        self._install_package(path)
