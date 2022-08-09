from os import path
from io import open
import re
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = re.sub('<script.*/script>', '', f.read())
    print(long_description)

with open(path.join(this_directory, 'world_trade_data/version.py')) as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    version = version_match.group(1)

setup(
    name='world_trade_data',
    version=version,
    author='Marc Wouts',
    author_email='marc.wouts@gmail.com',
    description='World Integrated Trade Solution (WITS) API in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mwouts/world_trade_data',
    packages=find_packages(exclude=['tests']),
    tests_require=['pytest'],
    install_requires=['pandas', 'requests', 'xmltodict'],
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Environment :: Console',
                 'Framework :: Jupyter',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10']
)
