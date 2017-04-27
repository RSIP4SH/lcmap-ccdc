import pytest
import glob
import json
import os
import itertools
from firebird.files import read

def flatten(iterable):
    """
    Reduce dimensionality of iterable containing iterables
    :param iterable: A multi-dimensional iterable
    :returns: A one dimensional iterable
    """
    return itertools.chain.from_iterable(iterable)

def chips(spectra, root_dir='./resources/data/chips/band-json'):
    """
    Return chips for named spectra
    :param spectra: red, green, blue, nir, swir1, swir2, thermal or cfmask
    :type spectra: string
    :returns: sequence of chips
    """
    path = ''.join([root_dir, os.sep, '*', spectra, '*'])
    filenames = glob.glob(path)
    chips = [json.loads(read(filename)) for filename in filenames]
    return flatten(chips)

def chip_specs(spectra, root_dir='./resources/data/chip-specs'):
    """
    Returns chip specs for the named spectra.
    :param spectra: red, green, blue, nir, swir1, swir2, thermal or cfmask
    :type spectra: string
    :returns: sequence of chip specs
    """
    path = ''.join([root_dir, os.sep, '*', spectra, '*'])
    filenames = glob.glob(path)
    return json.loads(read(filenames[0]))