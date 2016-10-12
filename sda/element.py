# -*- coding: utf-8 -*-
"""sda.element

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""


from lxml import html
from lxml.cssselect import CSSSelector, SelectorError
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSelectorException, TimeoutException
from shortcuts import encode_ascii


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.8.1'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Beta'
__docformat__ = 'reStructuredText'

__all__ = ['Element', 'normalize', 'join']


class Element(object):
    """The Element implementation

    An abstract class for interacting with web elements. Example use below:

    Example file structure:

    my_project
        - __init__.py
        - main.py
        - my_web_page
            - __init__.py
            - fixtures.py
            - locators.py
            - page.py


    The following example demonstrates a user creating a custom fixture (SomeElement) for an element on their web page,
    using a locator class to store the selenium selector and implement a web page view to interact with that web page
    and its elements:

    fixtures.py

    .. code-block:: python

        from selenium_data_attributes.element import Element
        from selenium_data_attributes.mixins import ClickMixin

        class SomeElement(Element, ClickMixin):

            pass


    locators.py

    .. code-block:: python

        from selenium_data_attributes.locators import Locators
        from selenium.webdriver.common.by import By

        class MyWebLocators(Locators):

            EXAMPLE_BUTTON = (By.XPATH, '//some//path[@id="id_example"])


    page.py

    .. code-block:: python

        from selenium_data_attributes.page import Page

        from my_project.my_web_page.fixtures import SomeElement
        from my_project.my_web_page.locators import MyWebLocators

        class MyWebPage(Page):

            def __init__(self, web_driver):

                self.driver = web_driver

                self.example_button = SomeElement(driver, *MyWebLocators.EXAMPLE_BUTTON)


    main.py

    .. code-block:: python

        from my_project.my_web_page.page import MyWebPage
        from selenium import webdriver

        # Instantiate webdriver
        wd = webdriver.Firefox()

        web_page = MyWebPage(wd)

        web_page.example_button.click()

    """

    def __init__(self, web_driver, by=By.XPATH, path=None, **kwargs):
        """Basic Selenium element

        :param WebDriver web_driver: Selenium webdriver
        :param str by: By selector
        :param str path: selection value
        :return:
        """

        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate selector
        self.search_term = normalize(by=by, path=path)

        # Add any additional attributes
        for extra in kwargs.keys():
            self.__setattr__(extra, kwargs[extra])

    def __contains__(self, attribute):
        """Returns True if element contains attribute

        :param str attribute: Element attribute
        :return: True, if the element contains that attribute
        :rtype: bool
        """

        if self.exists() and isinstance(attribute, basestring):

            source = self.outerHTML
            tree = html.fromstring(str(source))
            root = tree.xpath('.')

            if len(root) > 0:
                return True if 'required' in root[0].keys() else False

        return False

    @encode_ascii()
    def __getattr__(self, attribute):
        """Returns the value of an attribute

        :param str attribute: Element attribute
        :return: Returns the string value
        :rtype: str
        """

        if self.exists() and isinstance(attribute, basestring):

            # Special cases
            if attribute == "cls":
                attribute = "class"

            attribute = str(attribute).replace('_', '-')

            return self.element().get_attribute(attribute)

        return ''

    @encode_ascii()
    def __repr__(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        return self.outerHTML if self.exists() else ''

    def blur(self):
        """Simulate moving the cursor out of focus of this element.

        :return:
        """

        return self.driver.execute_script('arguments[0].blur();', self.element()) if self.is_displayed() else None

    @encode_ascii()
    def css_property(self, prop):
        """Return the value of a CSS property for the element

        .. warning::
            value_of_css_property does not work with Firefox

        :param str prop: CSS Property
        :return: Value of a CSS property
        :rtype: str
        """

        return self.element().value_of_css_property(str(prop)) if self.exists() else None

    def element(self):
        """Return the selenium webelement object

        :return: Selenium WebElement
        :rtype: WebElement
        """

        # If the search term passed through was an element
        if self.search_term[0] == 'element' and isinstance(self.search_term[1], WebElement):
            return self.search_term[1]

        # If the search term is a valid term
        elif self.search_term[0] in ('class name', 'css selector', 'id', 'link text',
                                     'name', 'partial link text', 'tag name', 'xpath'):

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

        return True if self.element() else False

    def focus(self):
        """Simulate element being in focus

        :return:
        """

        return self.driver.execute_script('arguments[0].focus();', self.element()) if self.is_displayed() else None

    def is_displayed(self):
        """Return True, if the element is visible

        :return: True, if element is visible
        :rtype: bool
        """

        return self.element().is_displayed() if self.exists() else False

    def scroll_to(self):
        """Scroll to the location of the element

        :return:
        """

        if self.exists():

            element = self.element()

            script = "var vHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);" \
                     "var eTop = arguments[0].getBoundingClientRect().top;" \
                     "window.scrollBy(0, eTop-(vHeight/2));"

            # Scroll to Element
            self.driver.execute_script(script, element)

    @property
    @encode_ascii()
    def tag_name(self):
        """Returns element tag name

        :return: Element tag name
        :rtype: str
        """

        return self.element().tag_name if self.exists() else ''

    def wait_until_present(self, timeout=30):
        """Wait until the element is present

        :param timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

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
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            if self.search_term[0] != 'element':

                wait.until(ec.invisibility_of_element_located(self.search_term))
                return True

        except TimeoutException:
            pass

        return False


def normalize(path, by=By.XPATH, *args, **kwargs):
    """

    :param str by: Selenium selector
    :param str path: Selector value
    :param args:
    :param kwargs:
    :return:
    """

    if args or kwargs:
        pass

    if by == 'class name':
        return By.XPATH, 'descendant-or-self::[contains(@class, "%s")]' % str(path)

    elif by == 'css selector':

        try:
            return CSSSelector(str(path)).path

        except SelectorError:
            pass

    elif by == 'element':
        if isinstance(path, Element):
            return By.XPATH, path.search_term

    elif by == 'id':
        return By.XPATH, 'descendant-or-self::[@id="%s"]' % str(path)

    elif by == 'link text':
        return By.XPATH, '(//a|//input|//button)[normalize-space(text()) = "%s"]' % str(path)

    elif by == 'name':
        return By.XPATH, 'descendant-or-self::*[@name="%s"]' % str(path)

    elif by == 'partial link text':
        return By.XPATH, '(//a|//input|//button)[contains(normalize-space(text()), "%s")]' % str(path)

    elif by == 'tag name':
        return By.XPATH, 'descendant-or-self::%s' % str(path)

    elif by == 'xpath':
        return by, path

    # All other cases return an empty statement
    return By.XPATH, ''


def join(*args):
    """Join 'x' locator paths into a single path

    :param args: Locator path tuples (by, path)
    :return: Locator path
    :rtype: str
    """

    return By.XPATH, '/'.join([normalize(*item)[1] for item in args if isinstance(item, (list, tuple))])
