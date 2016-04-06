"""
    selenium_data_attributes.site
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    This module implements an abstract object for the site as a whole
    
    :copyright: (c) 2016 FanThreeSixty
    :author: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE for more details.
"""

import re


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.3.5'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Site']


class Site(object):
    """Abstract class for a whole website
    """

    RE_URL = r'^(?:(?P<protocol>[a-zA-Z]+):\/\/)?(?P<base_url>[\w\d\.-]+\.[\w]{2,6})(?P<current_url>[\/\w\-\.\?]*)$'

    def __init__(self, driver):
        """

        :param driver: Selenium webdriver
        :return:
        """

        self.driver = driver
    
    @property
    def base_url(self):
        """Returns the base URL for a website
       
        :return: Base URL string
        :rtype: str
        """

        results = re.match(self.RE_URL, self.driver.current_url.encode('ascii', 'ignore'))

        try:
            return results.group("base_url")

        except IndexError:
            return ''
