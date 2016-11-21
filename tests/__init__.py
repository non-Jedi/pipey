import unittest
from .test_core import suite as core_suite

super_suite = unittest.TestSuite()

super_suite.addTests((core_suite,))
