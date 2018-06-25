import unittest

from openregistry.assets.core.constants import SANDBOX_MODE
from openregistry.assets.bounce.models import Asset


class TestSandBoxParameters(unittest.TestCase):

    @unittest.skipIf(not SANDBOX_MODE, 'If sandbox mode was\'t present')
    def test_parameter_is_present(self):
        sandbox_present = 'sandboxParameters' in Asset()._fields
        self.assertEqual(True, sandbox_present)
