from setuptools import setup
from pathlib import Path

version: str = "0.2.1-dev"
readme: str = (Path(__file__).parent / "README.md").read_text()
requirements: list = (Path(__file__).parent / "requirements.txt").read_text().splitlines()

packages: dict = [
    "src.pyrevolt",
    "src.pyrevolt.structs"
]

setup(
    name="pyrevolt",
    author="Fabio Almeida",
    author_email="me@fabioalmeida.dev",
    url="https://github.com/GenericNerd/pyrevolt",
    project_urls={
        "Source Code": "https://github.com/GenericNerd/pyrevolt",
        "Bug Tracker": "https://github.com/GenericNerd/pyrevolt/issues"
    },
    version=version,
    packages=packages,
    data_files=["requirements.txt"],
    license="MIT",
    description="A Python library to wrap the Revolt API, made to be easy-to-use but powerful and feature rich.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed"
    ]
)