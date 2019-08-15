# -*- coding: utf-8 -*-
import os
from setuptools import setup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "README.rst")) as f:
    long_description = f.read()

setup(
    name='sphinxcontrib-trimblank',
    version='1.0.1',
    description='A Sphinx extension which trims redundant blanks',
    long_description=long_description,
    url='https://github.com/amedama41/sphinxcontrib-trimblank',
    author='amedama41',
    author_email='kamo.devel41@gmail.com',
    keywords=['sphinx', 'extension'],
    packages=['sphinxcontrib'],
    namespace_packages=['sphinxcontrib'],
    install_requires=["Sphinx"],
    python_requires='>=3.5.*',
    classifiers=[
        'Framework :: Sphinx :: Extension',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx',
    ]
)
