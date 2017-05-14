import os

from setuptools import setup, find_packages

here = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read().strip().split()

setup(
    name='Movie Recommender',

    version='1.0.0',

    description='CMPE 297 Movie Recommendation Application',

    include_package_data=True,

    packages=find_packages(),

    py_modules=['server'],

    install_requires=requires,

    entry_points={
        'console_scripts': [
            'app = server:main'
        ]
    }
)
