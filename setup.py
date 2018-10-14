from setuptools import find_packages, setup

setup(
    name='powertac_logfiles',
    packages=find_packages('src'),
    version='0.0.1',
    description='Processing powertac logfiles',
    author='Niklas R.',
    package_dir={"": "src"},
)
