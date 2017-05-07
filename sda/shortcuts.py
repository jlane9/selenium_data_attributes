# -*- coding: utf-8 -*-
"""sda.shortcuts

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from selenium.webdriver.remote.webdriver import WebDriver
from sda.locators import Locators

__all__ = ['encode_ascii']


def encode_ascii(clean=False):
    """Function returns text as ascii

    :param clean: True, to delete trailing spaces
    :return:
    """

    def encode_ascii_decorator(func):
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

            text = func(*args, **kwargs)

            # Convert UNICODE to ASCII
            if isinstance(text, (str, unicode)):
                return text.encode('ascii', 'ignore').strip() if clean else text.encode('ascii', 'ignore')

            # Iterate list of UNICODE strings to ASCII
            elif isinstance(text, (list, tuple)):

                if clean:
                    return [item.encode('ascii', 'ignore').strip() for item in text
                            if isinstance(item, (str, unicode))]

                return [item.encode('ascii', 'ignore') for item in text
                        if isinstance(item, (str, unicode))]

            return ''

        return func_wrapper

    return encode_ascii_decorator


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
