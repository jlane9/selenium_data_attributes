"""Element

.. automodule:: sda.element
    :platform: Unix, Windows
    :synopsis: This module implements the core object used to create selenium structures.
    :copyright: (c) 2016 FanThreeSixty
    :moduleauthor: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE for more details.
"""

from core import DEFAULT_IDENTIFIER
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select as SeleniumSelect
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException, \
    InvalidSelectorException, TimeoutException


__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.4.3'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Element']


class Element(object):
    """Abstract web structure class
    """

    def __init__(self, web_driver, value, by=By.XPATH, identifier=DEFAULT_IDENTIFIER):
        """Basic Selenium element

        :param WebDriver web_driver: Selenium webdriver
        :param str by: By selector
        :param str value: selection value
        :return:
        """

        # Instantiate WebDriver
        if isinstance(web_driver, WebDriver):
            self.driver = web_driver

        else:
            self.driver = None
            raise TypeError("'web_driver' MUST be a selenium WebDriver element")

        # Instantiate selector
        if (By.is_valid(by) or by == 'element') and isinstance(value, str):
            self.search_term = (by, value)

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

            try:

                self.element().find_element_by_xpath('//self::*[@{0}]'.format(attribute))
                return True

            except NoSuchElementException:
                pass

        return False

    def __getattr__(self, attribute):
        """Returns the value of an attribute

        :param str attribute: Element attribute
        :return: Returns the string value
        :rtype: str
        """

        if self.exists():

            if attribute == "cls":
                    attribute = "class"

            attribute = attribute.replace('_', '-')

            try:
                return self.element().get_attribute(attribute).encode('ascii', 'ignore')

            except AttributeError:
                pass

        return ''

    def __repr__(self):
        """Returns HTML representation of the element

        :return: HTML representation of the element
        :rtype: str
        """

        if self.exists():
            return self.outerHTML

        return ''

    def angular_hidden(self):
        """Returns True if the element is hidden by angular

        :return: True, if the element is hidden by angular
        :rtype: bool
        """

        if 'ng-hide' in self.cls:
            return True

        return False

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

    def _click(self):
        """Click element

        :return:
        """

        if self.exists():

            try:
                self.element().click()

            # If the object is not within the view try to scroll to the element
            except (ElementNotVisibleException, WebDriverException):

                # Scroll to Element
                self._scroll_to()

                try:
                    self.element().click()

                except (ElementNotVisibleException, WebDriverException):
                    pass

    def _deselect_by_index(self, option):
        """Deselect option by index [i]

        :param option: Select option index
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                if isinstance(option, int) or isinstance(option, str):

                    # Convert string to integer
                    if isinstance(option, str):
                        if option.isdigit():
                            option = int(option)

                    select = SeleniumSelect(element)

                    try:
                        select.deselect_by_index(option)
                        return True

                    except NoSuchElementException:
                        pass

        return False

    def _deselect_by_text(self, option):
        """Deselect option by display text

        :param option: Select option
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, str):

                select = SeleniumSelect(element)

                try:

                    select.deselect_by_visible_text(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def _deselect_by_value(self, option):
        """Deselect option by option value

        :param option: Select option value
        :return: True, if option is deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, str):

                select = SeleniumSelect(element)

                try:

                    select.deselect_by_value(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def _deselect_all(self):
        """Deselect all selected options

        :return: True, if all options are deselected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)

                try:

                    select.deselect_all()
                    return True

                except NotImplementedError:
                    pass

        return False

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

    def _input(self, text, clear=True):
        """Send text to a input field

        :param str text: Text to send to the input field
        :param bool clear: True if user wants to clear the field before assigning text
        :return: True, if text is assigned
        :rtype: bool
        """

        if self.exists() and isinstance(text, str):

            element = self.element()

            if clear:
                element.clear()

            element.send_keys(text)

            return True

        return False

    def is_displayed(self):
        """Return True, if the element is visible

        :return: True, if element is visible
        :rtype: bool
        """

        if self.exists():
            return self.element().is_displayed()

        return False

    def _options(self):
        """Returns all Select options

        :return: List of options
        :rtype: list
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)

                options = []

                for option in select.options:
                    options.append(option.text.encode('ascii', 'ignore'))

                return options

        return []

    def _scroll_to(self):
        """Scroll to the location of the element

        :return:
        """

        # TODO: Need more intelligent scroll.
        if self.exists():

            element = self.element()

            # Scroll to Element
            self.driver.execute_script("window.scrollTo(0, %i)" % (element.location['y'] - element.size['height']))

    def _selected(self):
        """Return True if element is selected

        :return: True, if the element is selected
        :rtype: bool
        """

        if self.exists():
            return self.element().is_selected()

        return False

    def _selected_options(self):
        """Returns a list of selected options

        :return: List of options
        :rtype: list
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)
                options = []

                for option in select.all_selected_options:
                    options.append(option.text.encode('ascii', 'ignore'))

                return options

        return []

    def _selected_first(self):
        """Select first option

        :return:
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                select = SeleniumSelect(element)
                options = select.all_selected_options

                if len(options) > 0:
                    return options[0]

        return None

    def _select_by_index(self, option):
        """Select option at index [i]

        :param int option: Select index
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':

                if isinstance(option, int) or isinstance(option, str):

                    # Convert string to int
                    if isinstance(option, str):
                        if option.isdigit():
                            option = int(option)

                    select = SeleniumSelect(element)

                    try:

                        select.select_by_index(option)
                        return True

                    except NoSuchElementException:
                        pass

        return False

    def _select_by_text(self, option):
        """Select option by display text

        :param str option: Select option
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, str):

                select = SeleniumSelect(element)

                try:

                    select.select_by_visible_text(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def _select_by_value(self, option):
        """Select option by option value

        :param str option: Select option value
        :return: True, if the option is selected
        :rtype: bool
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select' and isinstance(option, str):

                select = SeleniumSelect(element)

                try:

                    select.select_by_value(option)
                    return True

                except NoSuchElementException:
                    pass

        return False

    def _text(self):
        """Returns the text within an element

        :return: Element text
        :rtype: str
        """

        if self.exists():

            element = self.element()
            text = element.text.encode('ascii', 'ignore').strip()

            if text == '':
                return element.get_attribute('textContent').encode('ascii', 'ignore').strip()

            return text

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

                wait.until(ec.presence_of_element_located(*self.search_term))
                return True

        except TimeoutException:
            pass

        return False

    def wait_until_disappears(self, timeout=30):
        """Wait until the element disappears

        :param timeout: Wait timeout in seconds
        :return:
        """

        if isinstance(timeout, int):
            wait = WebDriverWait(self.driver, timeout)

        else:
            wait = WebDriverWait(self.driver, 30)

        try:

            if self.search_term[0] != 'element':

                wait.until(ec.invisibility_of_element_located(*self.search_term))
                return True

        except TimeoutException:
            pass

        return False
