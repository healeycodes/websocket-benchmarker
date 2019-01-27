#!/usr/bin/env python

import unittest
import subprocess

# python environmental variable
python = 'python'

class EndToEnd(unittest.TestCase):

    def test_without_echo_server(self):
        echo_server = subprocess.Popen([python, 'echo_server.py', '--n', '64'])
        benchmarker = subprocess.Popen(
            [python, 'bench.py'], stdout=subprocess.DEVNULL)
        benchmarker.wait()
        echo_server.kill()
        assert(benchmarker.returncode == 1)


    def test_with_echo_server(self):
        echo_server = subprocess.Popen([python, 'echo_server.py', '--n', '64'])
        benchmarker = subprocess.Popen(
            [python, 'bench.py'], stdout=subprocess.DEVNULL)
        benchmarker.wait()
        echo_server.kill()
        assert(benchmarker.returncode == 0)

if __name__ == '__main__':
    unittest.main()
