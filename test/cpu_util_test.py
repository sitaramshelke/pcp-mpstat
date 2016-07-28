#!/usr/bin/env pmpython
import sys
import unittest
if sys.version_info[0] < 3:
    from mock import Mock
else:
    from unittest.mock import Mock
from pcp_mpstat import CpuUtil

class TestCpuUtil(unittest.TestCase):

    def current_values_side_effect(self, metric):
        if metric == 'hinv.map.cpu_num':
            return {1: 0, 2: 1}

    def test_get_percpu_util(self):
        metric_repository = Mock()
        cpu_util = CpuUtil(1.34, metric_repository)
        metric_repository.current_values = Mock(side_effect=self.current_values_side_effect)

        cpu_list = cpu_util.get_percpu_util()

        self.assertEqual(len(cpu_list),2)

    def test_get_totalcpu_util(self):
        metric_repository = Mock()
        cpu_util = CpuUtil(1.34, metric_repository)
        metric_repository.current_values = Mock(side_effect=self.current_values_side_effect)

        cpu_util = cpu_util.get_totalcpu_util()

        self.assertIsNotNone(cpu_util)

if __name__ == '__main__':
    unittest.main()
