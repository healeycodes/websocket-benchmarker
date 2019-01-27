#!/usr/bin/env python

import unittest
import subprocess
import warnings

# python environmental variable
python_env = 'python'


def ignore_resource_warning(func):
    '''Ignore any resource warnings produced by leaving echo_server running.'''

    def without_warn(self, *args, **kwargs):
        warnings.simplefilter("ignore", ResourceWarning)
        return func(self, *args, **kwargs)
    return without_warn


class EndToEnd(unittest.TestCase):
    def test_without_echo_server(self):
        '''The benchmark should error without the presense of an echo_server on `host` arg.'''

        result = subprocess.run(
            [python_env, 'bench.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert(result.returncode == 1)

    @ignore_resource_warning
    def test_with_echo_server(self):
        '''The benchmark should run without errors.'''

        echo_server = subprocess.Popen([python_env, 'echo_server.py', '--n', '64'])
        result = subprocess.run(
            [python_env, 'bench.py'], stdout=subprocess.DEVNULL)
        echo_server.kill()
        assert(result.returncode == 0)

    @ignore_resource_warning
    def test_stat_report(self):
        '''Statistics of the benchmark should be printed to stdout.'''

        echo_server = subprocess.Popen([python_env, 'echo_server.py', '--n', '64'])
        result = subprocess.Popen([python_env, 'bench.py'], stdout=subprocess.PIPE, shell=True)
        result.wait()
        output = str(result.stdout.read())
        echo_server.kill()
        assert('Min' in output)
        assert('Mean' in output)
        assert('Max' in output)


if __name__ == '__main__':
    unittest.main()
