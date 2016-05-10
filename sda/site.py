"""Site

.. automodule:: sda.site
    :synopsis: This module implements an abstract object for the site as a whole.
    :copyright: (c) 2016 FanThreeSixty
    :moduleauthor: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE.txt for more details.
"""

import re
from selenium.webdriver.remote.webdriver import WebDriver


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.4.3'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Site']


class Site(object):
    """Abstract class for a whole website
    """

    RE_URL = r'^(?:(?P<protocol>[a-zA-Z]+):\/\/)?(?P<base_url>[\w\d\.-]+\.[\w]{2,6})(?P<current_url>[\/\w\-\.\?]*)$'

    def __init__(self, web_driver):
        """Instantiate Site

        :param WebDriver web_driver: Selenium webdriver
        :return:
        """

        # Instantiate WebDriver
        if isinstance(web_driver, WebDriver):
            self.driver = web_driver

        else:
            self.driver = None
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")
    
    @property
    def base_url(self):
        """Returns the base URL for a website
       
        :return: Base URL string
        :rtype: str
        :raises NotImplementedError: If element driver is not a WebDriver
        """

        if isinstance(self.driver, WebDriver):
            results = re.match(self.RE_URL, self.driver.current_url.encode('ascii', 'ignore'))

        else:
            raise NotImplementedError("WebDriver was not instantiated!")

        try:
            return results.group("base_url")

        except IndexError:
            return ''
