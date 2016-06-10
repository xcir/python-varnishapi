# -*- encoding: utf-8 -*-

import os
import sys
from distutils.core import setup

from setuptools import find_packages

assert sys.version_info == (2, 7) or sys.version_info == (3, 4), "Python 2.7.x or 3.4.x is required."

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.rst')) as readme_file:
    long_description = readme_file.read()

sys.path.insert(0, current_dir + os.sep + 'src')

release = "0.1.0-initial"

setup(
    name='varnishapi',
    version=release,
    author='Shohei Tanaka(@xcir)',
    author_email='',
    description="Connect to libvarnish api by ctypes",
    long_description=long_description,
    install_requires=[],
    keywords='varnish,varnishlog,varnishstat',
    platforms=['any'],
    license='FreeBSD',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    zip_safe=False,
    zipfile=None,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
