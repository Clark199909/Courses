import unittest
from src.application import app
import json


class TestComposite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        print("SET UP Succeed!!")