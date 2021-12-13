""" Generate whilelist globals

Help:
python scripts/gen_whitelist.py --help
"""
import argparse
import logging

from model_unpickler import gen_pickle_whitelist


log = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbose', default=False, action='store_true',
    help="Show detailed log.")

args = parser.parse_args()

gen_pickle_whitelist()