from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'AMP tools for the PCMT Team'
LONG_DESCRIPTION = 'AMP tools for the PCMT Team, allowing to extract and split trajectories'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="amppcmt", 
        version=VERSION,
        author="Maxime Infuso",
        author_email="<maxime.infuso@univ-lille.fr",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'ase', 'amp-atomistics'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'amp', 'neural network', 'atomistics', 'PES'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
        ]
)
