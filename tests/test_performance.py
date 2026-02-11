import pytest
from unittest.mock import patch
from webtracker.utils.performance import timed_operation, create_performance_report


def test_timed_operation_returns_result():
    # Sample function to send through times_operations
    def sample_function(x, y):
        return x + y

    with patch('webtracker.utils.performance.db.save_performance_record'):
        result = timed_operation(sample_function, 5, 10)

    assert result == 15


def test_timed_operation_uses_function_name():
    # Test to see that timed operation sets the function name as operation name
    def test_operation():
        return "done"

    with patch('webtracker.utils.performance.db.save_performance_record') as mock_save:
        timed_operation(test_operation)

        call_args = mock_save.call_args[0]
        assert call_args[0] == 'test_operation'