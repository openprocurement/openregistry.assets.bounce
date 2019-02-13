from setuptools import setup, find_packages
import os

VERSION = '0.2.3'

entry_points = {
    'openregistry.assets.core.plugins': [
        'assets.bounce = openregistry.assets.bounce.includeme:includeme'
    ],
    'openregistry.tests': [
        'assets.bounce = openregistry.assets.bounce.tests.main:suite'
    ],
    'assets.bounce.migration': [
        'main = openregistry.assets.bounce.migration:migrate'
    ]
}

requires = [
    'setuptools',
    'openprocurement.api',
    'openregistry.assets.core'
]

test_requires = requires + []

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

setup(name='openregistry.assets.bounce',
      version=VERSION,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openregistry.assets.bounce',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openregistry', 'openregistry.assets'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'docs': docs_requires, 'test': test_requires},
      install_requires=requires,
      entry_points=entry_points,
      )
