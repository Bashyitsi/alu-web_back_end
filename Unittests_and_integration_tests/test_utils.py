#!/usr/bin/env python3
""" Test for utils.py """

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch
import requests


class TestAccessNestedMap(unittest.TestCase):
    """Test for access_nested_map"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """Test for access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path):
        """Test for Keyerror exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test for get_json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, url, payload):
        """Test for get_json with mock"""
        payload = {"payload": True}
        with patch.object(requests, "get") as mock:
            mock.return_value.json.return_value = payload
            self.assertEqual(get_json(url), payload)


class TestMemoize(unittest.TestCase):
    """Memoise test"""

    def test_memoize(self):
        """Memoize test"""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock:
            test = TestClass()
            test.a_property()
            test.a_property()
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
