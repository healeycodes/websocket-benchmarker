import os
import sys
import unittest
import subprocess
import warnings

# set python environmental variable
python_env = sys.executable


def get_path(file):
    '''Finds the path to the given local file in a cross-platform manner.'''

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(curr_dir, file)


def ignore_resource_warning(func):
    '''Ignore any resource warnings produced by leaving echo_server running.'''

    def without_warn(self, *args, **kwargs):
        warnings.simplefilter("ignore", ResourceWarning)
        return func(self, *args, **kwargs)
    return without_warn


class EndToEnd(unittest.TestCase):
    def test_without_echo_server(self):
        '''The benchmark should error without the presense of an echo_server on `host` arg.'''

        result = subprocess.run([python_env, get_path('bench.py')],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert(result.returncode == 1)

    @ignore_resource_warning
    def test_with_echo_server(self):
        '''The benchmark should run without errors.'''

        echo_server = subprocess.Popen([python_env, get_path('echo_server.py'), '--n', '64'],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = subprocess.run([python_env, get_path('bench.py')],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        echo_server.kill()
        assert(result.returncode == 0)

    @ignore_resource_warning
    def test_stat_report(self):
        '''Statistics of the benchmark should be printed to stdout.'''

        echo_server = subprocess.Popen([python_env, get_path('echo_server.py'), '--n', '64'],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result = subprocess.Popen([python_env, get_path('bench.py')],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        result.wait()
        output = str(result.stdout.read())
        echo_server.kill()
        assert('Min' in output)
        assert('Mean' in output)
        assert('Max' in output)


if __name__ == '__main__':
    unittest.main()
