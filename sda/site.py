"""Site
"""

from core import encode_ascii
import re
from selenium.webdriver.remote.webdriver import WebDriver


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.6.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Site']


class Site(object):
    """Abstract class for a whole website
    """

    RE_URL = r'^(?:(?P<protocol>[a-zA-Z]+):\/\/)?(?P<base_url>[\w\d\.-]+\.[\w]{2,6})(?P<current_url>[\/\w\-\.\?]*)$'

    def __init__(self, web_driver):
        """Website element

        :param WebDriver web_driver: Selenium webdriver
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
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
        """

        results = re.match(self.RE_URL, self.url)

        if results:

            try:
                return results.group("base_url")

            except IndexError:
                pass

        return ''

    @property
    @encode_ascii()
    def url(self):
        """Current page URL

        :return: Page URL
        :rtype: str
        """

        return self.driver.current_url
