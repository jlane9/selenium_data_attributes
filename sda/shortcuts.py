# -*- coding: utf-8 -*-
"""sda.shortcuts

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from __future__ import unicode_literals
from selenium.webdriver.remote.webdriver import WebDriver
from sda.locators import Locators

__all__ = ['generate_elements']


def generate_elements(_class, locator):
    """Iterate through all elements returned and create an instance of _class for each

    :param Element _class: Class to create instances from
    :param locator: SDA Locator. ex. ('xpath', '//element/path/here')
    :return:
    """

    def generate_elements_decorator(func):
        """

        :param func:
        :return:
        """

        def func_wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """

            web_driver = func(*args, **kwargs)

            # Make sure we receive a web driver and locator is a valid locator set
            if isinstance(web_driver, WebDriver) and (isinstance(locator, (list, tuple))):

                if len(locator) == 2:

                    if Locators.is_valid(*locator):

                        return [_class(web_driver=web_driver, by=locator[0], path='%s[%i]' % (locator[1], element+1))
                                for element in range(0, len(web_driver.find_elements(*locator)))]

                    raise TypeError("Error: Incorrect value for locator. ex. ('xpath', '//element/path/here')")

                else:
                    raise TypeError("Error: Incorrect value for locator. ex. ('xpath', '//element/path/here')")

            else:
                raise TypeError("Error: generate_elements requires the function to return a WebDriver object.")

        return func_wrapper

    return generate_elements_decorator
