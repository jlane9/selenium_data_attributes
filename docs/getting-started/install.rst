Installing SDA
--------------

sda (Selenium Data Attributes) is available on PyPi and on GitHub

PyPi
^^^^

To install via PyPi make sure you first install `Pip <https://pip.pypa.io/en/stable/installing/>`_
Afterwards run the following command in your terminal::

    sudo pip install sda


If you are having trouble installing the package use the following command::

    sudo pip install --no-dependencies sda


GitHub
^^^^^^

To install via Github you have two options for installers:
1. PyPi
2. Setuptools

To install sda using PyPi from Github you would run the following command::

    sudo pip install git+git://github.com/jlane9/selenium_data_attributes

You can add an additional `@branch-name` at the end to install from a specific branch

To install sda using Setuptools:

1. Make sure you have git cli (command line interface) installed on your machine
2. cd to the directory that you want the source to be installed and execute the following command::

    git clone https://github.com/jlane9/selenium_data_attributes

3. Move into that directory and install via setuptools::

    cd selenium_data_attributes
    sudo python setup.py install

Dependencies
^^^^^^^^^^^^

In case you are unable to install selenium from the dependencies, install using easy_install::

    sudo python easy_install selenium

And that's it! Selenium Data Attributes should be up and running!