"""
    selenium_data_attributes.page
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    This module implements an abstract object for a web page.
    
    :copyright: (c) 2016 FanThreeSixty
    :author: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE for more details.
"""

import re

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.2'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Page']


class Page(object):
    """Abstract class for a whole page
    """

    def __init__(self, driver, validation=""):
        """

        :param driver: Selenium webdriver
        :return:
        """

        self.driver = driver
        self._url_validation = validation

    def elements(self):
        """Returns all testable elements on a page
        
        :return: List of WebElements
        :rtype: list
        """
        return self.driver.find_elements_by_xpath('//*[@data-qa-id]')

    def in_view(self):
        """Returns True if the driver is currently within the scope of this page

        :return: True, if driver on page
        :rtype: bool
        """

        if self._url_validation != "":

            if len(re.findall(self._url_validation, self.url)) > 0:
                return True

            return False

        return True

    @property
    def title(self):
        """Return page title
        
        :return: Page title
        :rtype: str
        """
        
        return self.driver.title.encode('ascii', 'ignore')

    @property
    def url(self):
        """Current page URL
        
        :return: Page URL
        :rtype: str
        """
       
        return self.driver.current_url.encode('ascii', 'ignore')
