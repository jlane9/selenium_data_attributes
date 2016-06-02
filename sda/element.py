"""Element
"""

from core import DEFAULT_IDENTIFIER, encode_ascii
from lxml import html
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSelectorException, TimeoutException


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.6.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Element']


class Element(object):
    """Abstract web structure class
    """

    def __init__(self, web_driver, path, by=By.XPATH, identifier=DEFAULT_IDENTIFIER):
        """Basic Selenium element

        :param WebDriver web_driver: Selenium webdriver
        :param str by: By selector
        :param str path: selection value
        :return:
        """

        # Instantiate WebDriver
        if isinstance(web_driver, WebDriver):
            self.driver = web_driver

        else:
            self.driver = None
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate selector
        if (By.is_valid(by) or by == 'element') and isinstance(path, str):
            self.search_term = (by, path)

        else:
            self.search_term = (By.XPATH, "")

        # Instantiate identifier
        if isinstance(identifier, str):
            self._identifier = identifier

        else:
            self._identifier = DEFAULT_IDENTIFIER

    def __contains__(self, attribute):
        """Returns True if element contains attribute

        :param str attribute: Element attribute
        :return: True, if the element contains that attribute
        :rtype: bool
        """

        if self.exists() and isinstance(attribute, str):

            source = self.outerHTML
            tree = html.fromstring(source)
            root = tree.xpath('.')

            if len(root) > 0:
                if 'required' in root[0].keys():
                    return True

        return False

    @encode_ascii()
    def __getattr__(self, attribute):
        """Returns the value of an attribute

        :param str attribute: Element attribute
        :return: Returns the string value
        :rtype: str
        """

        if self.exists():

            # Special cases
            if attribute == "cls":
                    attribute = "class"

            attribute = attribute.replace('_', '-')

            return self.element().get_attribute(attribute)

        return ''

    @encode_ascii()
    def __repr__(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        if self.exists():
            return self.outerHTML

        return ''

    def blur(self):
        """Simulate moving the cursor out of focus of this element

        :return:
        """

        if self.exists():
            if self.is_displayed():
                self.driver.execute_script('arguments[0].blur();', self.element())

    def element(self):
        """Return the selenium webelement object

        :return: Selenium WebElement
        :rtype: WebElement
        """

        # If the search term passed through was an element
        if self.search_term[0] == 'element' and isinstance(self.search_term[1], WebElement):
            return self.search_term[1]

        # If the search term is a valid term
        elif By.is_valid(self.search_term[0]):

            try:

                # Locate element
                element = self.driver.find_elements(*self.search_term)

            except InvalidSelectorException:
                element = []

            if len(element) > 0:
                return element[0]

        return None

    def exists(self):
        """Returns True if element can be located by selenium

        :return: Returns True, if the element can be located
        :rtype: bool
        """

        element = self.element()

        if element:
            return True

        return False

    def focus(self):
        """Simulate element being in focus

        :return: 
        """

        if self.exists():
            if self.is_displayed():
                self.driver.execute_script('arguments[0].focus();', self.element())

    def is_displayed(self):
        """Return True, if the element is visible

        :return: True, if element is visible
        :rtype: bool
        """

        if self.exists():
            return self.element().is_displayed()

        return False

    def scroll_to(self):
        """Scroll to the location of the element

        :return:
        """

        # TODO: Need more intelligent scroll.
        if self.exists():

            element = self.element()

            # Scroll to Element
            self.driver.execute_script("window.scrollTo(0, %i)" % (element.location['y'] - element.size['height']))

    @property
    @encode_ascii()
    def tag_name(self):
        """Returns element tag name

        :return: Element tag name
        :rtype: str
        """

        if self.exists():
            return self.element().tag_name

        return ''

    def wait_until_present(self, timeout=30):
        """Wait until the element is present

        :param timeout: Wait timeout in seconds
        :return:
        """

        if isinstance(timeout, int):
            wait = WebDriverWait(self.driver, timeout)

        else:
            wait = WebDriverWait(self.driver, 30)

        try:

            if self.search_term[0] != 'element':

                wait.until(ec.presence_of_element_located(self.search_term))
                return True

        except TimeoutException:
            pass

        return False

    def wait_until_disappears(self, timeout=30):
        """Wait until the element disappears

        :param int timeout: Wait timeout in seconds
        :return:
        """

        if isinstance(timeout, int):
            wait = WebDriverWait(self.driver, timeout)

        else:
            wait = WebDriverWait(self.driver, 30)

        try:

            if self.search_term[0] != 'element':

                wait.until(ec.invisibility_of_element_located(self.search_term))
                return True

        except TimeoutException:
            pass

        return False
