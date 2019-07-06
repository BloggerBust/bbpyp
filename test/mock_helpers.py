from mock import call


def set_property_mock(mock, object_instance, new_value):
    mock.mock_calls.append(call(new_value))
    mock.call_count += 1
    mock.return_value = new_value
