#!/usr/bin/env python


import sys


def mul(a, b):
    """Multiply two numbers together. """
    return a * b


def main(args=None):
    """Read in command line arguments,
    and call the mul function.
    """
    if args is None:
        args = sys.argv[1:]

    if len(args) != 2:
        print('Usage: module_and_scripy.py a b')
        sys.exit(1)

    a = float(args[0])
    b = float(args[1])

    print('{} * {}: {}'.format(a, b, mul(a, b)))


# If this module is executed as a
# script, call the main function
if __name__ == '__main__':
    main()
