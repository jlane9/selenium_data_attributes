# -*- coding: utf-8 -*-
"""sda.page

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect
from urlparse import urlparse, urljoin
from sda.element import Element, SeleniumObject
from sda.shortcuts import encode_ascii

__all__ = ['Page']


class Page(SeleniumObject):
    """The Page Implementation
    """

    def __init__(self, web_driver, url_path="/"):
        """Web page element

        :param WebDriver web_driver: Selenium webdriver
        :param str url_path: URL path after net location
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        super(Page, self).__init__(web_driver)

        # Instantiate page-level URL validation
        self._url_path = url_path if isinstance(url_path, (str, unicode)) else "/"

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

        return self._url_path == urlparse(self.url).path

    @staticmethod
    def is_element(attrib=None):
        """Returns True if the class attribute is a valid locator

        :param attrib: Class attribute
        :return: True, if the class attribute is a valid locator
        :rtype: bool
        """

        return not(inspect.isroutine(attrib)) and isinstance(attrib, Element)

    def navigate_to(self):
        """Navigate to path

        :return:
        """

        if not self.in_view():

            current_url = urlparse(self.url)
            return self.driver.get(urljoin('{}://{}'.format(current_url.scheme, current_url.netloc), self._url_path))

        self.driver.refresh()

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
