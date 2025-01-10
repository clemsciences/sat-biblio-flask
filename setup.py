import os
import io
from setuptools import find_packages, setup

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(CUR_DIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()

with io.open(os.path.join(CUR_DIR, "LICENSE"), "r", encoding="utf-8") as f:
    LICENSE = f.read()

with open(os.path.join(CUR_DIR, "version.txt"), "r") as f:
    VERSION = f.read().strip()

setup(
    name='sat-biblio-web',
    version=VERSION,
    author='Clément Besnier',
    author_email='clem@clementbesnier.fr',
    description='Web app to manage library books.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/clemsciences/sat-biblio-flask',
    packages=find_packages(),
    include_package_data=True,
    keywords=['library', 'book', 'MARC', 'UNIMARC', 'INTERMARC'],
    scripts=[],
    exclude_package_data={'': ['doc', 'sat-biblio-interface', 'static']},
    zip_safe=True,
    python_requires=">=3.7",
    license=LICENSE,
)

