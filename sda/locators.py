# -*- coding: utf-8 -*-
"""sda.locators

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.8.1'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Beta'
__docformat__ = 'reStructuredText'

__all__ = ['is_iterable', 'Locators']


def is_iterable(obj):
    """Returns True

    :param obj: Object
    :return: True, if the object is tuple or a list
    :rtype: bool
    """

    return isinstance(obj, tuple) or isinstance(obj, list)


class Locators(object):
    """The Locators implementation
    """

    def as_dict(self):
        """Return all locators

        Example:

        .. code-block:: python

            from selenium_data_attributes.locators import Locators

            # Let's assume the user uses the Locators class to define some locators
            # for the elements on their web page.

            class SomeLocators(Locators):

                USER_NAME = (By.ID, 'username')
                PASSWORD = (By.ID, 'password')

            # If that user wanted to return all locators associated with this class
            # i.e. "USER_NAME" and "PASSWORD" and return the values of both
            # they'd use 'as_dict'

            l = SomeLocators()

            l.as_dict()

            # Returns
            # {'USER_NAME': (By.ID, 'username'), 'PASSWORD': (By.ID, 'password')}

        :return:
        :rtype: dict
        """

        return dict(inspect.getmembers(self, self.is_locator))

    @staticmethod
    def is_valid(by='', path=None):
        """Returns true if the selenium selector is valid

        :param str by: Selenium By locator
        :param str path: Locator value
        :return: True, if the selenium selector is valid
        :rtype: bool
        """

        return True if by in ('class name', 'css selector', 'id', 'link text',
                              'name', 'partial link text', 'tag name', 'xpath') and path else False

    def is_locator(self, attrib=None):
        """Returns True if the class attribute is a valid locator

        :param attrib: Class attribute
        :return: True, if the class attribute is a valid locator
        :rtype: bool
        """

        return self.is_valid(*attrib) if not(inspect.isroutine(attrib)) and is_iterable(attrib) else False
