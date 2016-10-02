from .context import pipey
from pipey.core import Network
import unittest

class ParsesSingleLineTestCase(unittest.TestCase):

    def setUp(self):
        self.network = Network()

    def test_parses_segment(self):
        self.network.parse(['segment 1'])
        self.assertEqual(self.network.segments[0].name, '1')

    def test_parses_node(self):
        self.network.parse(['node 1'])
        self.assertEqual(self.network.nodes[0].name, '1')
