from setuptools import find_packages, setup

setup(name='PyFrame',
      version='0.0',
      python_requires='==3.10',
      description='A simple animation framework for Python.',
      author='Tim Prokosch',
      author_email='prokosch@rhrk.uni-kl.de',
      packages=find_packages(include=['PyFrame'])
      )
