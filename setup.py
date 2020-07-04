#  python-fullmoon
#  ---------------
#  Determine the occurrence of the next full moon or to determine if a given 
#  date is/was/will be a full moon.
#
#  Author:  jr-k (c) 2020
#  Website: https://github.com/jr-k/python-fullmoon
#  License: MIT (see LICENSE file)

import codecs
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with codecs.open('fullmoon/__init__.py', 'r', 'utf-8') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='fullmoon',
    version=version,
    author='jrk',
    url='https://github.com/jr-k/python-fullmoon',
    packages=['fullmoon'],
    license='MIT',
    description='Determine the occurrence of the next full moon or to determine if a given date is/was/will be a full moon.',
    long_description=open('README.rst', encoding='utf-8').read(),
    long_description_content_type="text/x-rst",
    install_requires=[],
    platforms='any',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)