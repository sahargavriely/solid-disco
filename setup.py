from setuptools import setup, find_packages


setup(
    name='soliddisco',
    version='0.1.0',
    author='Sahar Gavriely',
    description='An example package.',
    packages=find_packages(),
    install_requires=['click', 'flask', 'werkzeug'],
    tests_require=['pytest', 'pytest-cov'],
)
