from setuptools import setup, find_packages

setup(
    name='eclipse_to_make',
    version='0.1',
    packages=find_packages(),
    extras_require={
        'test': ['pytest', 'mypy', 'flake8']
    },
    entry_points={
        'console_scripts': [
            'eclipse_to_make=eclipse_to_make:main',
        ],
    },
)
