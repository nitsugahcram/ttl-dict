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
    name="ttldict",
    version="1.0.0",
    description=("Python dict with TTL support for auto-expiring."),
    keywords='',
    license="MIT License",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'examples*']),
    url='/.git',
    author='Agustin March',
    author_email='agusti.march@gmail.com',
    long_description='Python application to consume tracess from'
    'the databus and classified that trace This'
    'package is intented to be used inside the smarttraces service.',
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=[
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6"
    ],
    cmdclass={
        'clean': CleanCommand,
    })
