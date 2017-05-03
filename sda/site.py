# -*- coding: utf-8 -*-
"""sda.site

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from urlparse import urlparse
from sda.element import SeleniumObject
from sda.shortcuts import encode_ascii

__all__ = ['Site']


class Site(SeleniumObject):
    """The Site Implementation

    The intention for the Site object is to contain all website pages. An example usage of this might be:

    Let's say we have the following file structure

    my_project
        - __init__.py
        - main.py
        - page_1
            - __init__.py
            - fixtures.py
            - locators.py
            - page.py
        - page_2
            - __init__.py
            - fixtures.py
            - locators.py
            - page.py

        - site
            - __init__.py
            - site.py
            - settings.py


    site/site.py

    .. code-block:: python

        from sda.site import Site
        from page_1.page import Page1
        from page_2.page import Page2

        class ExampleSite(Site):

            def __init__(self, web_driver):

                super(ExampleSite, self).__init__(web_driver)
                self.page_1 = Page1(web_driver)
                self.page_2 = Page2(web_driver)

    """

    @property
    def domain(self):
        """Returns the domain for a website

        :return: domain
        :rtype: str
        """

        return urlparse(self.url).netloc

    @property
    def path(self):
        """Returns the website path

        :return: path
        :rtype: str
        """

        return urlparse(self.url).path

    @property
    @encode_ascii()
    def url(self):
        """Current page URL

        :return: Page URL
        :rtype: str
        """

        return self.driver.current_url
