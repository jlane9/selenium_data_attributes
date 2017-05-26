# -*- coding: utf-8 -*-
"""sda.element

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import keyword
from lxml.cssselect import CSSSelector, SelectorError
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import InvalidSelectorException, TimeoutException, NoSuchElementException
from sda.shortcuts import encode_ascii

__all__ = ['Element', 'normalize', 'join']

DEFAULT_NAME_ATTR = 'data-qa-id'
DEFAULT_TYPE_ATTR = 'data-qa-model'


def normalize(_by, path, *args, **kwargs):
    """Convert all paths into a xpath selector

    :param str _by: Selenium selector
    :param str path: Selector value
    :param args:
    :param kwargs:
    :return:
    """

    if args or kwargs:
        pass

    xpath = '/descendant-or-self::*[{}]'

    normalizers = dict([
        ('class name', lambda x: xpath.format('contains(@class, "%s")' % x)),
        ('id', lambda x: xpath.format('@id="%s"' % x)),
        ('link text', lambda x: xpath.format('contains("input a button", name()) and '
                                             'normalize-space(text()) = "%s"' % x)),
        ('name', lambda x: xpath.format('@name="%s"' % x)),
        ('partial link text', lambda x: xpath.format('contains("input a button", name()) and '
                                                     'contains(normalize-space(text()), "%s")' % x)),
        ('tag name', lambda x: '/descendant-or-self::%s' % x),
        ('xpath', lambda x: x)
    ])

    if _by == 'css selector':

        try:
            return By.XPATH, '/%s' % CSSSelector(str(path)).path

        except SelectorError:
            return By.XPATH, ''

    elif _by == 'element':
        if isinstance(path, Element):
            return path.search_term

    else:
        return By.XPATH, normalizers.get(_by, lambda x: '')(str(path))


def join(*args):
    """Join 'x' locator paths into a single path

    :param args: Locator path tuples (by, path)
    :return: Locator path
    :rtype: str
    """

    return By.XPATH, ''.join([normalize(*item)[1] for item in args if isinstance(item, (list, tuple))])


class SeleniumObject(object):
    """The SeleniumObject implementation
    """

    def __init__(self, web_driver, **kwargs):

        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        if 'name_attr' in kwargs:
            self._name_attr = kwargs['name_attr'] if isinstance(kwargs['name_attr'], str) else DEFAULT_NAME_ATTR

        else:
            self._name_attr = DEFAULT_NAME_ATTR

        if 'type_attr' in kwargs:
            self._name_attr = kwargs['type_attr'] if isinstance(kwargs['type_attr'], str) else DEFAULT_TYPE_ATTR

        else:
            self._type_attr = DEFAULT_TYPE_ATTR

    def _wait_until(self, expected_condition, _by, path, timeout=30):
        """Wait until expected condition is fulfilled

        :param func expected_condition: Selenium expected condition
        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return:
        :rtype: bool
        """

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            if _by != 'element':

                wait.until(expected_condition((_by, path)))
                return True

        except TimeoutException:
            pass

        return False

    def wait_until_present(self, _by, path, timeout=30):
        """Wait until the element is available to the DOM

        :param str _by: Selector method
        :param str path: Selector path
        :param timeout: Wait timeout in seconds
        :return:
        :rtype: bool
        """

        return self._wait_until(ec.presence_of_element_located, _by, path, timeout)

    def wait_until_appears(self, _by, path, timeout=30):
        """Wait until the element appears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.visibility_of_element_located, _by, path, timeout)

    def wait_until_disappears(self, _by, path, timeout=30):
        """Wait until the element disappears

        :param str _by: Selector method
        :param str path: Selector path
        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.invisibility_of_element_located, _by, path, timeout)

    def wait_implicitly(self, seconds):
        """Wait a set amount of time in seconds

        :param int seconds: Seconds to wait
        :return:
        :rtype: bool
        """

        if isinstance(seconds, int):
            self.driver.implicitly_wait(seconds)
            return True

        return False


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

        # Instantiate web driver
        wd = webdriver.Firefox()

        web_page = MyWebPage(wd)

        web_page.example_button.click()

    """

    def __init__(self, web_driver, by=By.XPATH, path=None, **kwargs):
        """Basic Selenium element

        :param WebDriver web_driver: Selenium web driver
        :param str by: By selector
        :param str path: selection value
        :return:
        """

        self.driver = web_driver if isinstance(web_driver, WebDriver) else None

        if not self.driver:
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate selector
        self.search_term = normalize(_by=by, path=path)

        # Add any additional attributes
        for extra in kwargs:
            self.__setattr__(extra, kwargs[extra])

    def __contains__(self, attribute):
        """Returns True if element contains attribute

        :param str attribute: Element attribute
        :return: True, if the element contains that attribute
        :rtype: bool
        """

        if self.exists() and isinstance(attribute, (str, unicode)):

            try:
                self.driver.find_element(*join(self.search_term, ('xpath', '/self::*[boolean(@{})]'.format(attribute))))
                return True

            except NoSuchElementException:
                pass

        return False

    @encode_ascii()
    def __getattr__(self, attribute):
        """Returns the value of an attribute

        .. note:: class and for are both reserved keywords. Prepend/post-pend '_' to reference both.

        :param str attribute: Element attribute
        :return: Returns the string value
        :rtype: str
        """

        if self.exists():

            replacement = '' if keyword.iskeyword(attribute.replace('_', '')) else '-'
            return self.element().get_attribute(attribute.replace('_', replacement))

        return ''

    @encode_ascii()
    def __repr__(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        return '<{} by={} path={}>'.format(self.__class__.__name__, *self.search_term)

    def blur(self):
        """Simulate moving the cursor out of focus of this element.

        :return:
        """

        return self.driver.execute_script('arguments[0].blur();', self.element()) if self.is_displayed() else None

    @encode_ascii()
    def css_property(self, prop):
        """Return the value of a CSS property for the element

        :param str prop: CSS Property
        :return: Value of a CSS property
        :rtype: str
        """

        return self.element().value_of_css_property(str(prop)) if self.exists() else ''

    def drag(self, x_offset=0, y_offset=0):
        """Drag element x,y pixels from its center

        :param int x_offset: Pixels to move element to
        :param int y_offset: Pixels to move element to
        :return:
        """

        if self.exists() and isinstance(x_offset, int) and isinstance(y_offset, int):

            action = ActionChains(self.driver)
            action.click_and_hold(self.element()).move_by_offset(x_offset, y_offset).release().perform()
            return True

        return False

    def element(self):
        """Return the selenium web element object

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

            if element:
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

    def html(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        return self.outerHTML if self.exists() else ''

    def is_displayed(self):
        """Return True, if the element is visible

        :return: True, if element is visible
        :rtype: bool
        """

        return self.element().is_displayed() if self.exists() else False

    def parent(self):
        """Returns the Selenium element for the current element

        :return:
        """

        xpath = join(self.search_term, ('xpath', '/parent::*'))
        return Element(self.driver, xpath[0], xpath[1])

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

    def _wait_until(self, expected_condition, timeout=30):
        """Base function for wait functions

        :param expected_condition: Expected condition, callable must return boolean
        :param int timeout: Seconds before timeout
        :return:
        """

        wait = WebDriverWait(self.driver, timeout) if isinstance(timeout, int) else WebDriverWait(self.driver, 30)

        try:

            if self.search_term[0] != 'element' and callable(expected_condition):
                wait.until(expected_condition(self.search_term))
                return True

        except TimeoutException:
            return False

    def wait_until_present(self, timeout=30):
        """Wait until the element is present

        :param timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.presence_of_element_located, timeout)

    def wait_until_appears(self, timeout=30):
        """Wait until the element appears

        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.visibility_of_element_located, timeout)

    def wait_until_disappears(self, timeout=30):
        """Wait until the element disappears

        :param int timeout: Wait timeout in seconds
        :return: True, if the wait does not timeout
        :rtype: bool
        """

        return self._wait_until(ec.invisibility_of_element_located, timeout)
