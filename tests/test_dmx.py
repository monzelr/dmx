#!/usr/bin/env python

"""Tests for `dmx` package."""


import unittest

import time
import os
import numpy as np

import dmx


class TestDMX(unittest.TestCase):
    """Tests for `dmx` package."""

    @classmethod
    def setUpClass(cls):
        """
        setting up everything
        :return:
        """


    def setUp(self):
        """Set up test fixtures, if any."""

    @classmethod
    def tearDownClass(cls):
        """Tear down test fixtures, if any."""
        cls.disconnect()

    def test_DMX_(self):
        """Test dmx with numpy array"""
        pass

    @staticmethod
    def disconnect():
        pass
