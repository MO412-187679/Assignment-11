"""Find minimum weight cycle in 'weights.txt'."""
import os.path
import re


def path_to(filename: str):
    """Relative path to `filename` from current 'minweight.py' file."""
    try:
        basedir = os.path.dirname(__file__)
        fullpath = os.path.join(basedir, filename)
        return fullpath
    # some environemnts (like bpython) don't define '__file__',
    # so we assume that the file is in the current directory
    except NameError:
        return filename


def numeric_substring(text: str):
    """Removes leading '[' and trailing ']' alongside whitespace around it."""
    return text.strip().lstrip('[').rstrip(']').strip()


def read_weights(student: str, *, filename: str = path_to('weights.txt')):
    """Read weights from the provided file."""

    with open(filename, 'r') as file:
        matrices = (mat.strip() for mat in file.read().split('\n\n'))

    matrix, = (mat for mat in matrices if mat.startswith(student))
    name, weights = (text.strip() for text in matrix.split('\n', maxsplit=1))
    assert name == student

    return [
        [
            float(item.strip())
            for item in numeric_substring(line).split()
        ]
        for line in numeric_substring(weights).split('\n')
    ]


if __name__ == '__main__':
    from argparse import ArgumentParser

    # arguments
    parser = ArgumentParser('minweight.py')
    parser.add_argument('student', metavar='NAME', nargs='?',
        help='Student to solve.')

    args = parser.parse_args()
    student = args.student or 'Ti'

    # reading input
    weight_matrix = read_weights(student)
    raise NotImplementedError(weight_matrix)
