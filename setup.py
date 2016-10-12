from setuptools import setup, find_packages


setup(
    name='sda',
    version='0.8.1',
    packages=find_packages(),
    scripts=['scripts/sda-page'],
    description='A wrapper for Selenium. This library uses custom data attributes to accelerate testing '
    'through the Selenium framework',
    author='John Lane',
    author_email='jlane@fanthreesixty.com',
    url='https://github.com/jlane9/selenium-data-attributes',
    download_url='https://github.com/jlane9/selenium-data-attributes/tarball/0.8.1',
    keywords='testing selenium qa web automation',
    install_requires=[],
    license='MIT',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License',
                 'Topic :: Software Development :: Quality Assurance',
                 'Topic :: Software Development :: Testing'])
