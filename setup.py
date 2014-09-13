#!/usr/bin/env python

from setuptools import setup

setup(
    name='bp',
    version='0.5.0',
    description='A tool to quickly and easily clone project boilerplates',
    author='Ajay MT',
    author_email='ajaymt@icloud.com',
    url='http://github.com/code-boilerplates/bp',
    keywords='boilerplate code project clone tool template bp',
    py_modules=['bp'],
    requires=[
        'docopt (<1.0.0, >=0.6.2)'
    ],
    entry_points={
        'console_scripts': [
            'bp = bp:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
    ]
)
