import subprocess

import model_unpickler

try:
    import numpy as np
except ImportError:
    subprocess.run("pip install numpy>=1.16.2",
                   shell=True, check=True)
    import numpy as np

from os.path import realpath, dirname, join
from setuptools import find_packages
from distutils.core import setup


VERSION = model_unpickler.__version__
PROJECT_ROOT = dirname(realpath(__file__))

with open(join(PROJECT_ROOT, 'requirements.txt'), 'r') as f:
    install_reqs = f.read().splitlines()

long_description = """

A tool to load machine/deep learning models with security.

Many machine/deep learning libraries (PyTorch, Scikit-Learn and so on) save trained models solely based on Python pickle, while pickle is well known for its potential to execute malicious code when loading objects from untrusted sources.

This libary provides a secure tool to load pickled models by overriding the `find_class` method of standard python Unpickler class together with a series of global names -- __whilelist__. Only globals in the whilelist are allowed in loaded model objects, whereas the loading process interrupts when an untrusted global name is found to prevent any potential exploit.

This libary also provides utils to quickly update the global whilelist in case that the corresponding machine learning libraries are updated.

"""

setup(name='model-unpickler',
      version=VERSION,
      description='A tool to load machine/deep learning models with security',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/goeckslab/model-unpickler/',
      packages=find_packages(exclude=['docs', 'tests*', 'test-data*']),
      package_data={
          '': ['README.md',
               'requirements.txt']},
      include_package_data=True,
      install_requires=install_reqs,
      extras_require={'docs': ['mkdocs']},
      platforms='any',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Machine Learning',
          'Topic :: Scientific/Engineering :: Deep Learning',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ])