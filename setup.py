from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pdpp",
    version="0.4.8",
    install_requires=[
        'Click>=7.0', 
        'doit>=0.31.1', 
        'networkx>=2.2', 
        'graphviz>=0.10.1', 
        'pydot>=1.4.1', 
        'questionary>=1.0.2', 
        'pyyaml>=5.3'
        ],
    packages=find_packages(),
	include_package_data=True,
    entry_points = """
        [console_scripts]
        pdpp=pdpp.main:main
        """,
    readme="README.md",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Pierson Browne, Rachel Wood, Tyler Crick, John McLevey",
    author_email="pbrowne88@gmail.com",
    description="Command line tool for automation, transparency, and reproducibility in data processing projects",
    keywords="doit",
    url="https://github.com/UWNETLAB/pdpp",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
    ],		
)
