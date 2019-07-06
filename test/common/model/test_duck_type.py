import unittest
from mock import patch
from bbp.common.model.duck_type import DuckType


class TestDuckType(unittest.TestCase):
    def test_get_value_returns_expected_result(self):
        cases = [
            {"args": 10, "do_expand_args": False, "kwargs": None, "expected_result": 10},
            {"args": "test", "do_expand_args": False, "kwargs": None, "expected_result": "test"},
            {"args": ["1", 2, "three"], "do_expand_args": False,
                "kwargs": None, "expected_result": ["1", 2, "three"]},
            {"args": ["1", 2, "three"], "do_expand_args": True,
                "kwargs": None, "expected_result": ["1", 2, "three"]},
            {"args": None, "do_expand_args": False, "kwargs": {"number": 42, "string": f"foo", "child": {"number": 24, "string": "bar", "list": [1, "two", 3], "tupple1": (1), "tupple2": (1,), "tupple3": (1, "2", 3)}},
                "expected_result": {"number": 42, "string": "foo", "child": DuckType(**{"number": 24, "string": "bar", "list": [1, "two", 3], "tupple1": (1), "tupple2": (1,), "tupple3": (1, "2", 3)})}},
            {"args": {"number": 42, "string": "foo"}, "do_expand_args": False,
                "kwargs": None, "expected_result": {"number": 42, "string": "foo"}},
            {"args": 42, "do_expand_args": False, "kwargs": {"number": 42, "string": f"foo"},
                "expected_result": {"$value": 42, "number": 42, "string": "foo"}},
            {"args": ["1", 2, "three"], "do_expand_args": True, "kwargs": {"number": 42, "string": f"foo"},
                "expected_result": {"$value": ["1", 2, "three"], "number": 42, "string": "foo"}},
        ]

        case_number = 0
        for case in cases:
            args = case["args"]
            kwargs = case["kwargs"]
            expected_result = case["expected_result"]

            if args is not None and kwargs is None:
                result = DuckType(*args) if case["do_expand_args"] else DuckType(args)
            elif args is None and kwargs is not None:
                result = DuckType(**kwargs)
            elif args is not None and kwargs is not None:
                result = DuckType(
                    *args, **kwargs) if case["do_expand_args"] else DuckType(args, **kwargs)

            self.assertEqual(result.get_value(), expected_result,
                             f"case #{case_number} failed expectations")
            case_number += 1

    def test_is_atomic_returns_true_when_no_key_word_arguments_are_provided(self):
        cases = [
            {"args": 42, "kwargs": None, "is_atomic": True},
            {"args": None, "kwargs": {"name": "value"}, "is_atomic": False},
            {"args": "foo", "kwargs": {"name": "value"}, "is_atomic": False},
            {"args": {"thing": "value"}, "kwargs": {"name": "value"}, "is_atomic": False},
            {"args": {"name": "value"}, "kwargs": None, "is_atomic": True},
        ]

        for case in cases:
            args = case["args"]
            kwargs = case["kwargs"]

            result = DuckType(args, **kwargs) if kwargs else DuckType(args)
            self.assertEqual(result.is_atomic(), case["is_atomic"])

    def test_when_duck_type_is_not_atomic_key_arguments_become_properties(self):
        child = {"child": {"number": 24, "string": "bar", "number_list": [
            1, "two", 3], "tupple1": (1), "tupple2": (1,), "tupple3": (1, "2", 3)}}

        result = DuckType(number=42, string="foo", **child)

        child_result = DuckType(number=24, string="bar", number_list=[
                                1, "two", 3], tupple1=(1), tupple2=(1,), tupple3=(1, "2", 3))

        self.assertEqual(result.number, 42)
        self.assertEqual(result.string, "foo")
        self.assertEqual(result.child, child_result)
