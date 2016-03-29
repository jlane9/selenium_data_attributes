# from distutils.core import setup
from setuptools import setup, find_packages

setup(name='selenium-data-attributes',
      packages=find_packages(where="selenium_data_attributes"),
      version='0.2.3',
      description='A wrapper for Selenium. This library uses custom data attributes to accelerate testing '
                  'through the Selenium framework',
      author='John Lane',
      author_email='jlane@fanthreesixty.com',
      url='https://github.com/jlane9/selenium-data-attributes',
      download_url='https://github.com/jlane9/selenium-data-attributes/tarball/0.2',
      keywords='testing selenium qa web automation',
      install_requires=['selenium'],
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7'])
