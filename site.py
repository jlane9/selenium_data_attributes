"""Site - Automation Base class

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

__all__ = ['Site']


class Site(object):
    """Base object for all Dimension automation testing

    """

    RE_URL = r'^(?:(?P<protocol>[a-zA-Z]+):\/\/)?(?P<base_url>[\w\d\.-]+\.[\w]{2,6})(?P<current_url>[\/\w\-\.\?]*)$'

    def __init__(self, driver):
        """DimCore(driver) -> Selenium webdriver

        :param webdriver driver: Selenium webdriver
        :return:

        """

        self.driver = driver

    def base_url(self):

        results = re.match(self.RE_URL, self.driver.current_url.encode('ascii', 'ignore'))

        try:
            return results.group("base_url")

        except IndexError:
            return ''
