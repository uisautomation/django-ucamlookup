#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-ucamlookup',
    description='A Django module for the University of Cambridge Lookup service',
    long_description=open('README.rst').read(),
    url='https://github.com/uisautomation/django-ucamlookup.git',
    version='1.9.5',
    license='MIT',
    author='Information Systems Group, University Information Services, University of Cambridge',
    author_email='devops@uis.cam.ac.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.8'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
