import unittest
from mock import Mock, patch

from bbpyp.common.service.metric_service import MetricService


@patch('test.TestContext', create=True)
class TestMetricService(unittest.TestCase):

    def setUp(self):
        self._values = [13, 18, 13, 14, 13, 16, 14, 21, 13]

        #self.maxDiff = None

    def test_is_initialized_as_expected(self, test_context):
        metric_service = MetricService(test_context.named_item_service)
        self.assertIs(test_context.named_item_service, metric_service._named_item_service)

    def test_get_qualified_name_returns_as_expected(self, test_context):
        name = "foo"
        expected_qualified_name = f"{name}.{MetricService.POSTFIX}"
        metric_service = MetricService(test_context.named_item_service)
        actual_qualified_name = metric_service.get_qualified_name(name)
        self.assertEqual(expected_qualified_name, actual_qualified_name)

    def test_get_frequency_table_returns_as_expected(self, test_context):
        name = "foo"
        expected_qualified_name = f"{name}.{MetricService.POSTFIX}"
        test_context.named_item_service.get_with_validation.return_value = test_context.frequency_table

        metric_service = MetricService(test_context.named_item_service)
        actual_frequency_table = metric_service.get_frequency_table(name)

        self.assertIs(test_context.frequency_table, actual_frequency_table)
        test_context.named_item_service.get_with_validation.assert_called_once_with(
            expected_qualified_name, "No metrics have been recorded.")

    def test_set_frequency_table_sets_as_expected(self, test_context):
        name = "foo"
        expected_qualified_name = f"{name}.{MetricService.POSTFIX}"

        metric_service = MetricService(test_context.named_item_service)
        metric_service.set_frequency_table(name, test_context.frequency_table)

        test_context.named_item_service.set.assert_called_once_with(
            expected_qualified_name, test_context.frequency_table)

    def test_get_values_returns_values_in_indexed_order(self, test_context):
        frequency_table = {3: test_context.mock_frequency, 5: test_context.mock_frequency,
                           8: test_context.mock_frequency, 2: test_context.mock_frequency, 54: test_context.mock_frequency, 45: test_context.mock_frequency}
        expected_values = list(frequency_table.keys())
        with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_frequency_table", return_value=frequency_table) as get_frequency_table_mock:
            metric_service = MetricService(test_context.named_item_service)
            actual_values = metric_service.get_values("foo")
            self.assertEqual(expected_values, actual_values)

    def test_get_sorted_values_returns_values_in_sorted_order(self, test_context):
        values = [5, 7, 8, 1, 4, 10, 2, 6, 87]
        expected_sorted_values = sorted(values)
        with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_values", return_value=values) as get_values_mock:
            metric_service = MetricService(test_context.named_item_service)
            actual_sorted_values = metric_service.get_sorted_values("foo")
            self.assertEqual(expected_sorted_values, actual_sorted_values)

    def test_get_max_value_returns_as_expected(self, test_context):
        values = [5, 7, 8, 1, 4, 10, 2, 6, 87]
        expected_max_value = 87
        with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_values", return_value=values) as get_values_mock:
            metric_service = MetricService(test_context.named_item_service)
            actual_max_value = metric_service.get_max_value("foo")
            self.assertEqual(expected_max_value, actual_max_value)

    def test_get_min_value_returns_as_expected(self, test_context):
        values = [5, 7, 8, 1, 4, 10, 2, 6, 87]
        expected_min_value = 1
        with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_values", return_value=values) as get_values_mock:
            metric_service = MetricService(test_context.named_item_service)
            actual_min_value = metric_service.get_min_value("foo")
            self.assertEqual(expected_min_value, actual_min_value)

    def test_get_range_returns_as_expected(self, test_context):
        min_value = 23
        max_value = 87
        expected_range = max_value - min_value
        with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_max_value", return_value=max_value) as get_max_value_mock, patch(f"{MetricService.__module__}.{MetricService.__name__}.get_min_value", return_value=min_value) as get_min_value_mock:
            metric_service = MetricService(test_context.named_item_service)
            actual_range = metric_service.get_range("foo")
            self.assertEqual(expected_range, actual_range)

    def test_get_mean_returns_as_expected(self, test_context):
        cases = [
            ([], lambda values: None),
            ([5, 7, 8, 1, 4, 10, 2, 6, 87], lambda values: sum(values) / len(values))
        ]
        for case in cases:
            values, calculate = case
            expected_mean = calculate(values)
            with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_values", return_value=values) as get_values_mock:
                metric_service = MetricService(test_context.named_item_service)
                actual_mean = metric_service.get_mean("foo")
                self.assertEqual(expected_mean, actual_mean)

    def test_get_median_returns_as_expected(self, test_context):
        cases = [
            ([], None),
            ([1], 1),
            ([1, 2, 4, 8, 10, 32, 87], 8),
            ([3, 5], 4),
            ([1, 2, 4, 8, 10, 32], 6),
            ([1, 2, 4, 9, 10, 32], 6.5),
        ]

        for case in cases:
            values, expected_median = case
            with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_sorted_values", return_value=values) as get_values_mock:
                metric_service = MetricService(test_context.named_item_service)
                actual_median = metric_service.get_median("foo")
                self.assertEqual(expected_median, actual_median)

    def test_get_mode_returns_as_expected(self, test_context):
        freq = test_context.mock_frequency
        expected_freq = test_context.expected_mock_frequency
        cases = [
            ([], None),
            ([(1, expected_freq)], (1, expected_freq)),
            ([(1, expected_freq), (3, freq), (5, freq), (7, freq),
              (9, freq), (56, freq)], (1, expected_freq)),
            ([(56, expected_freq), (1, freq), (5, freq), (99, freq)], (56, expected_freq))
        ]
        for case in cases:
            most_common_result, expected_mode = case
            test_context.frequency_table.most_common.return_value = most_common_result
            with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_frequency_table", return_value=test_context.frequency_table) as get_frequency_table_mock:
                metric_service = MetricService(test_context.named_item_service)
                actual_mode = metric_service.get_mode("foo")
                self.assertEqual(expected_mode, actual_mode)

    def test_get_least_frequent_returns_as_expected(self, test_context):
        freq = test_context.mock_frequency
        expected_freq = test_context.expected_mock_frequency
        cases = [
            ([], None),
            ([(1, expected_freq)], (1, expected_freq)),
            ([(1, freq), (3, freq), (5, freq), (7, freq),
              (9, freq), (56, expected_freq)], (56, expected_freq)),
            ([(56, freq), (1, freq), (5, freq), (99, expected_freq)], (99, expected_freq))
        ]
        for case in cases:
            most_common_result, expected_least_frequent = case
            test_context.frequency_table.most_common.return_value = most_common_result
            with patch(f"{MetricService.__module__}.{MetricService.__name__}.get_frequency_table", return_value=test_context.frequency_table) as get_frequency_table_mock:
                metric_service = MetricService(test_context.named_item_service)
                actual_least_frequent = metric_service.get_least_frequent("foo")
                self.assertEqual(expected_least_frequent, actual_least_frequent)
