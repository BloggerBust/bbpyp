from collections import Counter


class MetricService:
    POSTFIX = "metric"

    def __init__(self, named_item_service):
        self._named_item_service = named_item_service

    def record_numeric_value(self, name, value):
        self.record_numeric_values(name, [value])

    def record_numeric_values(self, name, value):
        frequency_table = self.get_frequency_table(name) if self.has(name) else Counter()
        frequency_table.update(value)
        self.set_frequency_table(name, frequency_table)

    def get_mode(self, name):
        frequency_table = self.get_frequency_table(name)
        most_to_least_common = frequency_table.most_common()
        return most_to_least_common[0] if len(most_to_least_common) > 0 else None

    def get_least_frequent(self, name):
        frequency_table = self.get_frequency_table(name)
        most_to_least_common = frequency_table.most_common()
        length = len(most_to_least_common)
        return most_to_least_common[length - 1] if length > 0 else None

    def get_median(self, name):
        ordered_keys = self.get_sorted_values(name)
        length = len(ordered_keys)
        if length == 0:
            return None

        if length % 2 == 0:
            first_index = int(length / 2) - 1
            second_index = int(length / 2)
            median = (ordered_keys[first_index] + ordered_keys[second_index]) / 2
        else:
            middle_index = int((length + 1) / 2) - 1
            median = ordered_keys[middle_index]

        return median

    def get_mean(self, name):
        values = self.get_values(name)
        length = len(values)
        if length == 0:
            return None

        return sum(values) / length

    def get_max_value(self, name):
        ordered_keys = self.get_values(name)
        length = len(ordered_keys)
        if length == 0:
            return None

        return max(ordered_keys)

    def get_min_value(self, name):
        ordered_keys = self.get_values(name)
        length = len(ordered_keys)
        if length == 0:
            return None

        return min(ordered_keys)

    def get_range(self, name):
        max_value = self.get_max_value(name)
        if max_value is None:
            return None
        return max_value - self.get_min_value(name)

    def get_frequency_table(self, name):
        return self._named_item_service.get_with_validation(self.get_qualified_name(name), "No metrics have been recorded.")

    def set_frequency_table(self, name, frequency_table):
        self._named_item_service.set(self.get_qualified_name(name), frequency_table)

    def get_sorted_values(self, name):
        values = self.get_values(name)
        return sorted(values)

    def get_values(self, name):
        frequency_table = self.get_frequency_table(name)
        return list(frequency_table.keys())

    @classmethod
    def get_qualified_name(cls, name):
        return f"{name}.{cls.POSTFIX}"

    def has(self, name):
        return self._named_item_service.has(self.get_qualified_name(name))

    @property
    def names(self):
        return [metric_name.rstrip(f".{self.POSTFIX}") for metric_name in self._named_item_service.names]

    def length(self, name):
        return len(self.get_frequency_table(name))
