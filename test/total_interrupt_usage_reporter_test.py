import unittest
from mock import Mock
from pcp_mpstat import TotalInterruptUsageReporter

class TestTotalInterruptUsageReporter(unittest.TestCase):

    def test_print_report(self):
        timestamp = "2016-19-07 IST"
        total_interrupt_usage = Mock()
        total_interrupt_usage.total_interrupt_per_delta_time = Mock(return_value = 1.23)
        options = Mock()
        printer = Mock()
        report = TotalInterruptUsageReporter(total_interrupt_usage, printer, options)

        report.print_report(timestamp)

        printer.assert_called_with('2016-19-07 IST\t  all\t 1.23')


if __name__ == "__main__":
    unittest.main()     