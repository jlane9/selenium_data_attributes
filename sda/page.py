"""Page
"""

from element import *
import inspect
import re
from shortcuts import encode_ascii
from selenium.webdriver.remote.webdriver import WebDriver

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.7.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Page']


class Page(object):
    """The Page Implementation
    """

    def __init__(self, web_driver, validation=""):
        """Web page element

        :param WebDriver web_driver: Selenium webdriver
        :param str validation: regular expression to check URL
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate page-level URL validation
        self._url_validation = validation if isinstance(validation, str) else ""

    def elements(self):
        """Returns all testable elements on a page
        
        :return: Dictionary of WebElements
        :rtype: dict
        """

        return dict(inspect.getmembers(self, self.is_element))

    def in_view(self):
        """Returns True if the driver is currently within the scope of this page

        :return: True, if driver on page
        :rtype: bool
        """

        return len(re.findall(self._url_validation, self.url)) == 0 if self._url_validation != "" else False

    @staticmethod
    def is_element(attrib=None):
        """Returns True if the class attribute is a valid locator

        :param attrib: Class attribute
        :return: True, if the class attribute is a valid locator
        :rtype: bool
        """

        return not(inspect.isroutine(attrib)) and isinstance(attrib, Element)

    @property
    @encode_ascii()
    def title(self):
        """Return page title
        
        :return: Page title
        :rtype: str
        """
        
        return self.driver.title

    @property
    @encode_ascii()
    def url(self):
        """Current page URL
        
        :return: Page URL
        :rtype: str
        """
       
        return self.driver.current_url
