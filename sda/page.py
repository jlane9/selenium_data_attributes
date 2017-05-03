# -*- coding: utf-8 -*-
"""sda.page

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect
from urlparse import urlparse
from sda.element import Element, SeleniumObject
from sda.shortcuts import encode_ascii

__all__ = ['Page']


class Page(SeleniumObject):
    """The Page Implementation
    """

    def __init__(self, web_driver, validation=""):
        """Web page element

        :param WebDriver web_driver: Selenium webdriver
        :param str validation: regular expression to check URL
        :return:
        :raises TypeError: If web_driver is not a Selenium WebDriver
        """

        super(Page, self).__init__(web_driver)

        # Instantiate page-level URL validation
        self._url_validation = str(validation) if isinstance(validation, basestring) else ""

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

        page_url = ''.join([urlparse(self._url_validation).netloc, urlparse(self._url_validation).path])
        current_url = ''.join([urlparse(self.url).netloc, urlparse(self.url).path])

        return page_url == current_url if page_url != "" else True

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
