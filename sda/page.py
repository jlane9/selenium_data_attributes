# -*- coding: utf-8 -*-
"""sda.page

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from __future__ import unicode_literals
import inspect
import re
from six import string_types
from sda.element import Element, SeleniumObject

try:
    from urlparse import urljoin, urlparse
except (ImportError, ModuleNotFoundError):
    from urllib.parse import urljoin, urlparse


__all__ = ['Page']


class Page(SeleniumObject):
    """The Page Implementation
    """

    def __init__(self, web_driver, url_path="/"):
        """Web page element

        :param WebDriver web_driver: Selenium webdriver
        :param str url_path: URL path after net location. Use Open API spec
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        super(Page, self).__init__(web_driver)

        # Instantiate page-level URL validation
        self._url_path = url_path if isinstance(url_path, string_types) else "/"

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

        return bool(re.match('^' + re.sub(r'(:\w+)', '.+', self._url_path) + '$', urlparse(self.url).path))

    @staticmethod
    def is_element(attrib=None):
        """Returns True if the class attribute is a valid locator

        :param attrib: Class attribute
        :return: True, if the class attribute is a valid locator
        :rtype: bool
        """

        return not(inspect.isroutine(attrib)) and isinstance(attrib, Element)

    def navigate_to(self, *args):
        """Navigate to path

        :return:
        """

        try:
            path = re.sub(r'(:\w+)', '{}', self._url_path).format(*args)

        except IndexError:
            raise IndexError('URL path does not contain the correct number of args')

        if not self.in_view():

            current_url = urlparse(self.url)
            return self.driver.get(urljoin('{}://{}'.format(current_url.scheme, current_url.netloc), path))

        self.driver.refresh()

    @property
    def title(self):
        """Return page title

        :return: Page title
        :rtype: str
        """

        return self.driver.title

    @property
    def url(self):
        """Current page URL

        :return: Page URL
        :rtype: str
        """

        return self.driver.current_url
