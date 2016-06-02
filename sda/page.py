"""Page
"""

from core import *
import re
from selenium.webdriver.remote.webdriver import WebDriver

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.6.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Page']


class Page(object):
    """Abstract class for a web page
    """

    def __init__(self, web_driver, validation="", identifier=DEFAULT_IDENTIFIER):
        """Web page element

        :param WebDriver web_driver: Selenium webdriver
        :param str validation: regular expression to check URL
        :param str identifier: Tag identifier
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        # Instantiate WebDriver
        if isinstance(web_driver, WebDriver):
            self.driver = web_driver

        else:
            self.driver = None
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate page-level URL validation
        if isinstance(validation, str):
            self._url_validation = validation

        else:
            self._url_validation = ""

        # Instantiate identifier
        if isinstance(identifier, str):
            self._identifier = identifier

        else:
            self._identifier = DEFAULT_IDENTIFIER

    def elements(self):
        """Returns all testable elements on a page
        
        :return: List of WebElements
        :rtype: list
        """

        return self.driver.find_elements_by_xpath('//*[@{0}]'.format(self._identifier))

    def in_view(self):
        """Returns True if the driver is currently within the scope of this page

        :return: True, if driver on page
        :rtype: bool
        """

        if self._url_validation != "":
            if len(re.findall(self._url_validation, self.url)) == 0:
                return False

        return True

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
