#!/usr/bin/env python3
import re

from setuptools import setup

with open('readme.md', 'r', encoding='utf-8') as f:
    README = f.read()

with open('uaparser/__init__.py', 'r', encoding='utf-8') as f:
    VERSION = re.search(r"__version__ = '(.+)'", f.read()) \
        .group(1)

setup(
    name='ua-parser-py',
    version=VERSION,
    python_requires='>=3.6',
    description='Python library to detect Browser, Engine, OS, CPU, and Device type/model from User-Agent data',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/vitalibo/ua-parser-py',
    author='Vitaliy Boyarsky',
    author_email='boyarsky.vitaliy@live.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='user-agent parser browser engine os device cpu',
    packages=['uaparser'],
    data_files=[('', ['license.md', 'readme.md'])],
    zip_safe=False,
    install_requires=[],
    platforms='any'
)
