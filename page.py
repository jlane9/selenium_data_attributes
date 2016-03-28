"""Page - Automation Base class

.. module:: core
   :platform: Unix, Windows
   :synopsis:

.. moduleauthor:: John Lane <jlane@fanthreesixty.com>

"""

import re

__author__ = 'jlane'
__copyright__ = 'Copyright (C) FanThreeSixty'
__contact__ = 'jlane@fanthreesixty.com'
__docformat__ = 'reStructuredText'

__all__ = ['Page']


class Page(object):
    """Base object for all Dimension automation testing

    """

    def __init__(self, driver, validation=""):
        """

        :param webdriver driver: Selenium webdriver
        :return:

        """

        self.driver = driver
        self._url_validation = validation

    def elements(self):
        return self.driver.find_elements_by_xpath('//*[@data-qa-id]')

    def in_view(self):
        """Returns True if the driver is currently within the scope of this page

        :return:
        """

        if self._url_validation != "":

            if len(re.findall(self._url_validation, self.url)) > 0:
                return True

            return False

        return True

    @property
    def title(self):
        return self.driver.title.encode('ascii', 'ignore')

    @property
    def url(self):
        return self.driver.current_url.encode('ascii', 'ignore')

    def url_validation(self):
        return re.findall(self._url_validation, self.url)
