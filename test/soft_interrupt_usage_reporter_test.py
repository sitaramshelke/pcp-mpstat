import unittest
from mock import Mock
from mock import call
from pcp_mpstat import SoftInterruptUsageReporter

class TestSoftInterruptUsageReporter(unittest.TestCase):
	def setUp(self):
		self.interrupts = [ Mock(), Mock()]
		self.interrupts[0].configure_mock(
							name = Mock(return_value = 'SOME_INTERRUPT'),
							value = Mock(return_value = 1.23))
		self.interrupts[1].configure_mock(
							name = Mock(return_value = 'ANOTHER_INTERRUPT'),
							value = Mock(return_value = 2.34))
		self.cpu_interrupt_zero = Mock(
								cpu_number = 0,
								interrupts = self.interrupts
								)
	def test_print_report(self):
		soft_interrupt_usage = Mock()
		printer = Mock()
		options = Mock()
		cpu_interrupts = [self.cpu_interrupt_zero]
		soft_interrupt_usage.get_percpu_interrupts = Mock(return_value = cpu_interrupts)
		report = SoftInterruptUsageReporter(soft_interrupt_usage, printer, options)
		timestamp = '2016-7-18 IST'
		calls = [call(' Timestamp\t cpu\tSOME_INTERRUPT/s\tANOTHER_INTERRUPT/s\t'),
 				call('2016-7-18 IST\t   0\t            1.23\t               2.34\t')]

		report.print_report(timestamp)

		printer.assert_has_calls(calls, any_order = False)

if __name__ == '__main__':
	unittest.main()