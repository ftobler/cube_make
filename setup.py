from setuptools import setup, find_packages

setup(
    name='cube_make',
    version='0.1',
    packages=find_packages(),
    extras_require={
        'test': ['pytest', 'mypy', 'flake8']
    },
    entry_points={
        'console_scripts': [
            'cube_make=cube_make:main',
        ],
    },
)
