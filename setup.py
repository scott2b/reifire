"""
Setup script for reifire
"""
from setuptools import setup
from pathlib import Path

def read_requirements(filename: str) -> list[str]:
    """Read requirements from file."""
    print(f"Looking for requirements in: {Path(filename).absolute()}")
    try:
        reqs = [line.strip() 
                for line in Path(filename).read_text().splitlines()
                if line.strip() and not line.startswith('#')]
        print(f"Found requirements: {reqs}")
        return reqs
    except FileNotFoundError:
        print(f"WARNING: Could not find {filename}")
        return []  # Return empty list if file not found

setup(
    packages=["reifire"],
    package_dir={"": "src"},
    install_requires=read_requirements('requirements.txt'),
    include_package_data=True,
) 