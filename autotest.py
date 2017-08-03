#!/usr/bin/env python3

"""An autotest script for COMP1521.
Written by Gal Aharon (2017)
"""

import argparse
from difflib import SequenceMatcher
import glob


_colours = {'red':'\x1b[0;31m{}\x1b[0m', 'green':'\x1b[0;32m{}\x1b[0m'}

BASE_DIR = '~z5164705/public_html/tests/'

for key in _colours:
    vars()[key] = lambda x : x 

def gen_colours():
    for key in _colours:
        # dynamically create coloured functions because im lazy and also we can do stuff
        def func(string):
            return _colours[key].format(string)
        vars()[key] = func 

def diff(actual, expected):
    # modified from code by tzot - https://stackoverflow.com/a/788780/4073852
    changed = False
    output = []
    seqm = SequenceMatcher(None, a, b)
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            changed = True
            output.append(green(seqm.b[b0:b1]))
        elif opcode == 'delete':
            changed = True
            output.append(red(seqm.a[a0:a1]))
        elif opcode == 'replace':
            changed = True
            output.append(red(seqm.a[a0:a1]) + green(seqm.b[b0:b1]))
        else:
            raise RuntimeError('Unexpected OpCode "%s"' % (opcode,))
    return ''.join(output) if changed else None



def sanitise_args(args):
    """Makes sure the passed in arguments are a-ok!"""
    # make sure args.class exists or else print error message
    # make sure args.lab exists or else print error message
    # if args.exercise is not '' make sure file exists
    # if args.test is not blank make sure test exists
    
def run_tests(cls, lab, exercise, test, challenge):
    exercise_dirs = [BASE_DIR + exercise + '/'] if exercise else glob.glob(BASE_DIR + '*/')
    for exercise_dir in exercise_dirs:
        test_files = [exercise_dir + test] if tets else glob.glob(exercise_dir + '*.json')
        for test_file in test_files:
            test = Test(test_file)
            test.run()
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cls', action='store', help='Class which the test belong to.')
    parser.add_argument('lab', action='store', help='The lab to run tests for.')
    parser.add_argument('--exercise', action='store', default='', help='The file to run tests for. By default will run on all applicable files.')
    parser.add_argument('--test', action='store', default='', help='A specific test to run. By default runs all tests.')
    parser.add_argument('--challenge', action='store_true', default=False, help='Use this flag to run challenge as well as regular autotests.')
    parser.add_argument('--no_colour', action='store_true', default=False, help='Turns off colourising in the terminal.')
    
    args = parser.parse_args()
    
    sanitise_args(args)
    
    if not args.no_colour:
        gen_colours()
    
    run_tests(args.cls, args.lab, args.exercise, args.test, args.challenge)