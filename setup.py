import os

from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as fp:
        return fp.read()


setup(
    name='checklisting',
    version='0.1b1',
    description='Web crawlers for downloading bird checklists.',
    long_description=read("README.rst"),
    author='Stuart MacKay',
    author_email='smackay@flagstonesoftware.com',
    url='http://pypi.python.org/pypi/checklisting/',
    license='GPL',
    packages=find_packages(),
    keywords='eBird worldbirds web crawler birds checklists',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Natural Language :: English",
        "Topic :: Text Processing :: Filters",
    ],
    install_requires=[
        'scrapy',
    ],
)
