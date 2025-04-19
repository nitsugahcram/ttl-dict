"""Setup the package creation and installation."""
import os
from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""

    user_options = []

    def initialize_options(self):  # noqa
        pass

    def finalize_options(self):  # noqa
        pass

    def run(self):  # noqa
        os.system('rm -vrf ./build ./dist '  # nosec
                  './*.pyc ./*.tgz ./*.egg-info')


setup(
    zip_safe=True,
    name="ttl-dict",
    version="1.0.2",
    description=("Python dict with TTL support for auto-expiring."),
    keywords='',
    license="MIT License",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'examples*']),
    url='git@github.com:nitsugahcram/ttl-dict.git',
    author='Agustin March',
    author_email='agusti.march@gmail.com',
    long_description='',
    python_requires='>=3.8,<4',
    install_requires=[
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.11"
    ],
    cmdclass={
        'clean': CleanCommand,
    })
