import logging
import os
import unittest

logging.basicConfig(format="%(asctime)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s",
                    handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class TestProjectCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_no_location(self):
        """No location provided."""
        pass

    def test_invalid_location(self):
        """Invalid location."""
        pass

    def test_valid_location(self):
        """Valid location."""
        pass
