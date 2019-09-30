import sys

try:
    from setuptools import setup
except ImportError:
    sys.exit("The python library 'setuptools' need to be installed!")

setup(
    name='GenSkew',
    version='0.1',
    url='https://github.com/hanneskramml/GenSkew',
    license='GPL-3.0',
    author='Hannes Kramml',
    author_email='hannes@kramml.com',
    description='Genomic nucleotide skew application',
    # long_description=readme(),
    # package_dir={'genskew': 'src'},
    packages=['genskew', 'genskew.cli'],
    install_requires=[
        'biopython',
        'matplotlib'
    ],
    extras_require={
        'WebGUI': ['genskew.web', 'flask', 'flask-kvsession', 'jsonpickle']
    },
    include_package_data=True,
    package_data={
        'genskew.web': ['static/*', 'templates/*'],
    },
    entry_points={'console_scripts': ['genskew = genskew.cli.cli:main']}
)
