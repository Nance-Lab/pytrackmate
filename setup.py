from setuptools import setup, find_packages

setup(
    name="pytrackmate",
    version="0.1",
    packages=find_packages(include=["pytrackmate", "pytrackmate.*"]),  # Explicitly include only your package
    install_requires=[
        # List your dependencies here
    ],
)
