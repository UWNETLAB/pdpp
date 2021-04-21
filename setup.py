from setuptools import setup, find_packages

setup(
    name="pdpp",
    version="0.4.3",
    install_requires=['Click>=7.0', 'doit>=0.31.1', 'networkx>=2.2', 'graphviz>=0.10.1', 'pydot>=1.4.1', 'questionary>=1.0.2', 'pyyaml>=5.3'],
    packages=find_packages(),
	include_package_data=True,
    entry_points = """
        [console_scripts]
        pdpp=pdpp.main:main
        """,

    author="Pierson Browne, Rachel Wood, Tyler Crick, John McLevey",
    author_email="pbrowne88@gmail.com",
    description="Command line tool for automation, transparency, and reproducibility in data processing projects",
    keywords="doit",
    url="http://networkslab.org",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
    ],		
)
