#!/usr/bin/env python

from setuptools import setup

setup(
    name='boilerplate',
    version='0.0.1',
    description='A tool to quickly and easily clone project boilerplates',
    author='Ajay MT',
    author_email='ajaymt@icloud.com',
    url='http://github.com/code-boilerplates/boilerplate',
    keywords='boilerplate code project clone tool template',
    py_modules=['boilerplate'],
    requires=[
        'docopt (<1.0.0, >=0.6.2)'
    ],
    entry_points={
        'console_scripts': [
            'boilerplate = boilerplate'
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
