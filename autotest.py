#!/usr/bin/env python3

"""An autotest script for COMP1521.
Written by Gal Aharon (2017)
"""

from argparse import ArgumentParser
from difflib import SequenceMatcher
import glob
import json
import os
import subprocess

# base directory which contains all the test files
BASE_DIR = os.path.expanduser('~z5164705/public_html/tests/')
# colour functions for printing text to console. Example usage print(colours['red']('...'))
colours = {'red': lambda s : '\x1b[0;31m{}\x1b[0m'.format(s), 'green': lambda s : '\x1b[0;32m{}\x1b[0m'.format(s)}

def dir_name(pathstring):
    """Returns the directory name from a directory path:
    e.g. last_directory('/a/b/c/') = 'c'
    """
    return os.path.basename(os.path.normpath(pathstring))

def diff(actual, expected):
    """Returns a diff string if the two string were different which is already colourised.
    If both inputs are the same, returns None.
    
    Modified from code by tzot - https://stackoverflow.com/a/788780/4073852
    """
    changed = False
    output = []
    seqm = SequenceMatcher(None, actual, expected)
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            changed = True
            output.append(colours['green'](seqm.b[b0:b1]))
        elif opcode == 'delete':
            changed = True
            output.append(colours['red'](seqm.a[a0:a1]))
        elif opcode == 'replace':
            changed = True
            output.append(colours['red'](seqm.a[a0:a1]) + colours['green'](seqm.b[b0:b1]))
        else:
            raise RuntimeError('Unexpected OpCode "{}"'.format(opcode))
    return ''.join(output) if changed else None

class Test:
    """A class that represents a single test supplied in JSON file format.
    For examples look at ~z5164705/public_html/tests
    
        Arguments:
            test_file - a path to the json file containing the test's information.
            working_directory - a path to the working directory in which the binary
                                executable for the test can be found.
                                
        Attributes:
            name - the name of the test. (optional)
            description - a short description of the test. (optional)
            exercise - the exercise in the lab that this test belongs to. (optional)
            challenge - whether or not the test is considered a challenge.
            time_limit - the time limit of the test in seconds. (optional)
            binary - the path to the executable file which will run this test.
            args - command line arguments to pass to the binary. (optional)
            input - the input this test will deliver to the binary.
            expected - the expected output of this test.
            diff - an empty string if the test passed or has not been run, otherwise
                    a colourised diff between the expected and actual output.
            authors - a list of authors who contributed the test
    """
    def __init__(self, test_file, working_directory):
        def get_optional(data, key, default=None):  # helper method
            return data[key] if key in data else default
        
        with open(test_file) as f:
            data = json.load(f)
            self.name = get_optional(data, 'name', os.path.splitext(os.path.basename(test_file))[0])
            self.description = get_optional(data, 'description', 'no description')
            self.exercise = get_optional(data, 'exercise', data['binary'])
            self.challenge = get_optional(data, 'challenge', False)
            self.time_limit = get_optional(data, 'time_limit', 60)
            self.binary = working_directory + '/' + data['binary']
            self.args = [str(arg) for arg in get_optional(data, 'args', [])]
            self.input = [line + '\n' for line in data['input']]
            self.expected = ''.join([line + '\n' for line in data['expected']])
            self.diff = ''
            self.authors = get_optional(data, 'authors', ['no author'])
        if not os.path.isfile(self.binary):
            print('You are missing the required file: {}'.format(data['binary']))
            print('Have you compiled your code?')
            exit()

    def run(self):
        """Runs the autotest. Diff will be stored in self.diff"""
        process = subprocess.Popen([self.binary] + self.args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        for line in self.input:
            process.stdin.write(line.encode())
        try:
            out, err = process.communicate(timeout=self.time_limit)  # TODO test timeout
            if err:
                self.diff = """Encountered error running test:
                Output: {}
                Error output: {}
                """.format(out.decode(), err.decode())
            else:
                self.diff = diff(out.decode(), self.expected)  # TODO make sure I didn't break diff
        except subprocess.TimeoutExpired:
            self.diff = colours['red']('Time limit exceeded.')
    
    def show_diff(self):
        """Shows the diff if there is one."""
        if diff:
            print()
            print(self.diff)
    
def validate_args(args):
    """Makes sure the passed in arguments are a-ok!"""
    if not os.path.isdir(BASE_DIR + args.cls):
        print('{} is not a recognised class'.format(args.cls))
        print('Valid classes: {}'.format([dir_name(x) for x in glob.glob(BASE_DIR + '*/')]))
        exit()
    if not os.path.isdir(BASE_DIR + args.cls + '/' + args.lab):
        print('{} is not a valid lab number.'.format(args.lab))
        print('Valid labs: {}'.format([dir_name(x) for x in glob.glob(BASE_DIR + '/' + args.cls + '/*/')]))
        exit()
        
def load_tests(directory, exercise='', test_name='', challenge=False):
    """Loads all json test files from the given directory.
    If exercise or test name is set, ony matching tests are returned.
    If challenge is True then challenge tests will not be ignored.
    """
    tests = []
    files = glob.glob(directory + '*.json')
    if not files:
        print('There are no tests currently available for this lab.')
        exit()
    for test_file in files:
        test = Test(test_file, os.getcwd())
        if (exercise and test.exercise != exercise
                or test_name and test.name != test_name
                or not challenge and test.challenge):
            continue
        else:
            tests.append(test)
    if not tests and (exercise or test_name):
        print('No tests matched the given conditions. Use -l to list all available exercises.')
        exit()
    return tests
    
def run_tests(tests):
    failed_tests = []
    for test in tests:
        print('{} - ({}) '.format(test.name, test.description), end='')
        test.run()
        if test.diff:
            print(colours['red']('Failed'))
            test.show_diff()
            failed_tests.append(test.name)
        else:
            print(colours['green']('Passed'))
    
    print('Passed {}/{} tests.'.format(len(tests) - len(failed_tests), len(tests)))
    if failed_tests:
        print(colours['red']('Tests failed {}'.format(failed_tests)))
    else:
        print(colours['green']('You passed all the tests! You are awesome! :)'))
        

if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('cls', action='store', help='Class which the test belong to.')
    parser.add_argument('lab', action='store', help='The lab to run tests for.')
    parser.add_argument('-e', '--exercise', action='store', default='', help='The file to run tests for. By default will run on all applicable files.')
    parser.add_argument('-t', '--test', action='store', default='', help='A specific test to run. By default runs all tests.')
    parser.add_argument('-c', '--challenge', action='store_true', default=False, help='Use this flag to run challenge as well as regular autotests.')
    parser.add_argument('--no_colour', action='store_true', default=False, help='Turns off colourising in the terminal.')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='Lists all tests and exercises available.')
    
    args = parser.parse_args()
    validate_args(args)
    if args.list:
        print('Valid exercises: {}'.format(
            set(test.exercise for test in load_tests(BASE_DIR + args.cls + '/' + args.lab + '/'))))
        exit()
    if args.no_colour:
        colours = dict.fromkeys(colours.keys(), lambda x : x)
    run_tests(load_tests(BASE_DIR + args.cls + '/' + args.lab + '/', args.exercise, args.test, args.challenge))