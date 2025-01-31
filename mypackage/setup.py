#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 23:30:56 2024

@author: isisboelens
"""

from setuptools import setup, find_packages

setup(
    name='web-citation-extractor',  # Name of your package
    version='0.1',  # Version of the package
    packages=find_packages(),  # Automatically discover packages in the directory
    install_requires=[  # External dependencies
        'selenium', 
        'beautifulsoup4', 
        'requests', 
        'urllib3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',  # Ensure compatibility with Python 3
        'License :: OSI Approved :: MIT License',  # Licensing
        'Operating System :: OS Independent',  # Ensures cross-platform compatibility
    ],
    python_requires='>=3.6',  # Python version requirement
    description='A Python tool to extract URLs and generate APA citations from webpages.',
    author='Isis Boelens',  # Your name
    author_email='ifboelens@tudelft.nl',  # Your email address (replace with your actual one)
    url='https://github.com/ifboelens/Gitlab-Proposal',  # GitHub or project URL
    long_description_content_type='text/markdown',  # Specify the type of the long description (Markdown)
    include_package_data=True,  # Ensures that additional files like README.md are included in the package
)
