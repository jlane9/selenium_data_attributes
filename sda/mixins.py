# -*- coding: utf-8 -*-
"""sda.mixins

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from sda.shortcuts import encode_ascii
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select as SeleniumSelect
from selenium.common.exceptions import ElementNotVisibleException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

__all__ = ['ClickMixin', 'InputMixin', 'SelectMixin', 'SelectiveMixin', 'TextMixin']


def to_int(value):
    """Coerce string to int

    :param str value: String integer
    :return:
    :rtype: int
    """

    if isinstance(value, (str, unicode, int)):

        if isinstance(value, (str, unicode)):

            if value.isdigit():
                return int(value)

        else:
            return value


class ElementMixin(object):
    """The ElementMixin Implementation

    .. note::
        This is a dummy class.
    """

    def __getattr__(self, item):
        return item

    # This function will be overridden by the base class this extends
    def blur(self):
        """Simulate moving out of focus

        :return:
        """

        if self:
            pass

    # This function will be overridden by the base class this extends
    def element(self):
        """Returns the element

        :return:
        """

        return WebElement(WebDriver(), 'html') if self.exists() else None

    # This function will be overridden by the base class this extends
    def exists(self):
        """Return True if the element exists

        :return:
        """

        if self:
            pass

    def is_disabled(self):
        """Returns True, if the element is disabled

        :return: True, if the element is disabled
        :rtype: bool
        """

        return self.__contains__('disabled')

    # This function will be overridden by the base class this extends
    def scroll_to(self):
        """Simulate scrolling to element

        :return:
        """

        if self:
            pass


class ClickMixin(ElementMixin):
    """The ClickMixin Implementation
    """

    def click(self):
        """Click element

        :return:
        """

        element = self.element()

        if element:

            try:

                if not element.is_displayed():
                    self.scroll_to()

                element.click()
                return True

            except (ElementNotVisibleException, WebDriverException):
                pass

        return False

    def double_click(self):
        """Double-click element

        :return:
        """

        element = self.element()

        if element:

            try:

                if not element.is_displayed():
                    self.scroll_to()

                return ActionChains(self.driver).double_click(element).perform()

            except (ElementNotVisibleException, WebDriverException):
                pass

    def hover(self):
        """Simulate hovering over element

        :return:
        """

        element = self.element()

        if element:

            try:

                if not element.is_displayed():
                    self.scroll_to()

                return ActionChains(self.driver).move_to_element(element).perform()

            except (ElementNotVisibleException, WebDriverException):
                pass


class InputMixin(ElementMixin):
    """The InputMixin implementation
    """

    def __str__(self):
        return self.value

    def input(self, *args, **kwargs):
        """

        :param args: Text to send to the input field
        :param kwargs: clear - True if user wants to clear the field before assigning text
        :return: True, if text is assigned
        :rtype: bool
        """

        element = self.element()

        if element:

            if 'clear' in kwargs:
                element.clear()

            element.send_keys(*args)

            return True

        return False

    @property
    @encode_ascii()
    def value(self):
        """Return value of input

        :return: Input value
        :rtype: str
        """

        return self.element().get_attribute('value') if self.exists() else ''

    @value.setter
    def value(self, value):

        if self.exists():
            self.driver.execute_script('arguments[0].value = arguments[1]', self.element(), str(value))


class SelectMixin(ElementMixin):
    """The SelectMixin implementation
    """

    def _get_selenium_select(self):
        """Returns a SeleniumSelect representation of a select element

        :return:
        :rtype: SeleniumSelect
        """

        if self.exists():

            element = self.element()

            if element.tag_name == u'select':
                return SeleniumSelect(element)

    def deselect_all(self):
        """Deselect all selected options

        :return: True, if all options are deselected
        :rtype: bool
        """

        select = self._get_selenium_select()

        if select:

            select.deselect_all()
            return True

        return False

    def deselect_by_index(self, option):
        """Deselect option by index [i]

        :param option: Select option index
        :return: True, if option is deselected
        :rtype: bool
        """

        select = self._get_selenium_select()
        option = to_int(option)

        if select and isinstance(option, int):

            try:

                select.deselect_by_index(option)
                return True

            except NoSuchElementException:
                pass

        return False

    def deselect_by_text(self, option):
        """Deselect option by display text

        :param option: Select option
        :return: True, if option is deselected
        :rtype: bool
        """

        select = self._get_selenium_select()

        if select and isinstance(option, (str, unicode)):

            try:

                select.deselect_by_visible_text(option)
                return True

            except NoSuchElementException:
                pass

        return False

    def deselect_by_value(self, option):
        """Deselect option by option value

        :param option: Select option value
        :return: True, if option is deselected
        :rtype: bool
        """

        select = self._get_selenium_select()

        if select and isinstance(option, (str, unicode)):

            try:

                select.deselect_by_value(option)
                return True

            except NoSuchElementException:
                pass

        return False

    def options(self):
        """Returns all Select options

        :return: List of options
        :rtype: list
        """

        select = self._get_selenium_select()
        options = []

        if select:

            for option in select.options:
                options.append(option.text.encode('ascii', 'ignore'))

        return options

    def selected_first(self):
        """Select first option

        :return: First option element
        :rtype: WebElement
        """

        selected = self.selected_options()

        return selected[0] if selected else None

    def selected_options(self):
        """Returns a list of selected options

        :return: List of options
        :rtype: list
        """

        select = self._get_selenium_select()
        options = []

        if select:
            options = [option.text.encode('ascii', 'ignore') for option in select.all_selected_options]

        return options

    def select_by_index(self, option):
        """Select option at index [i]

        :param str option: Select index
        :return: True, if the option is selected
        :rtype: bool
        """

        select = self._get_selenium_select()
        option = to_int(option)

        if select and isinstance(option, int):

            try:

                select.select_by_index(option)
                return True

            except NoSuchElementException:
                pass

        return False

    def select_by_text(self, option):
        """Select option by display text

        :param str option: Select option
        :return: True, if the option is selected
        :rtype: bool
        """

        select = self._get_selenium_select()

        if select and isinstance(option, (str, unicode)):

            try:

                select.select_by_visible_text(option)
                return True

            except NoSuchElementException:
                pass

        return False

    def select_by_value(self, option):
        """Select option by option value

        :param str option: Select option value
        :return: True, if the option is selected
        :rtype: bool
        """

        select = self._get_selenium_select()

        if select and isinstance(option, (str, unicode)):

            try:

                select.select_by_value(option)
                return True

            except NoSuchElementException:
                pass

        return False


class SelectiveMixin(ClickMixin):
    """The SelectiveMixin implementation
    """

    def deselect(self):
        """Deselect this element

        :return:
        """

        return self.click() if self.selected() else False

    def select(self):
        """Select this element

        :return:
        """

        return self.click() if not self.selected() else False

    def selected(self):
        """Return True if element is selected

        :return: True, if the element is selected
        :rtype: bool
        """

        return self.element().is_selected() if self.exists() else False


class TextMixin(ElementMixin):
    """The TextMixin implementation
    """

    def __str__(self):
        return self.text()

    @encode_ascii(clean=True)
    def text(self):
        """Returns the text within an element

        :return: Element text
        :rtype: str
        """

        return self.element().get_attribute('textContent') if self.exists() else ''

    @encode_ascii(clean=True)
    def visible_text(self):
        """Returns the visible text within an element

        :return: Element text
        :rtype: str
        """

        return self.element().text if self.exists() else ''
