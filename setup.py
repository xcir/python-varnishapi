# -*- encoding: utf-8 -*-

import os
import sys
from distutils.core import setup

from setuptools import find_packages

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.rst')) as readme_file:
    long_description = readme_file.read()

sys.path.insert(0, current_dir + os.sep + 'src')

release = "40.12"

setup(
    name='varnishapi',
    version=release,
    author='Shohei Tanaka(@xcir)',
    author_email='kokoniimasu@gmail.com',
    url='https://github.com/xcir/python-varnishapi',
    description="Connect to libvarnish api by ctypes",
    long_description=long_description,
    install_requires=[],
    keywords='varnish,varnishlog,varnishstat',
    platforms=['any'],
    license='BSD',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    py_modules = ['varnishapi'],
    zip_safe=False,
    zipfile=None,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
