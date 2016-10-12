# -*- coding: utf-8 -*-
"""sda.fixtures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from element import *
import inspect
from mixins import *
from shortcuts import encode_ascii
from selenium.webdriver.common.by import By

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.8.1'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Beta'
__docformat__ = 'reStructuredText'

__all__ = ['Dropdown', 'DropdownMenu', 'List', 'Search', 'SearchBox', 'SpectrumColorPicker', 'TabNavigation']


class SpectrumColorPicker(Element):
    """The SpectrumColorPicker implementation
    """

    def input(self, color):
        """Send text to a input field

        :param str color: Color to send to the input field
        :return: True, if text is assigned
        :rtype: bool
        """

        if self.exists() and (isinstance(color, str) or isinstance(color, unicode)):

            self.driver.execute_script('$(arguments[0]).spectrum("set", arguments[1]);', self.element(), color)
            return True

        return False

    @encode_ascii()
    def value(self):
        """Return value of input

        :return: Input value
        :rtype: str
        """

        return self.element().get_attribute('value') if self.exists() else ''


class Dropdown(Element, DropdownMixin):
    """Abstract class for dropdown elements

    Example:

        This implementation should cover most cases for a dropdown.


    locators.py

    .. code-block:: python

        from selenium_data_attributes.locators import Locators
        from selenium.webdriver.common.by import By

        class MyPageLocators(Locators):

            DROPDOWN = (By.ID, "id_dropdown")
            DROPDOWN_CONTAINER = (By.ID, "id_dropdown_container")


    fixtures.py

    .. code-block:: python

        from selenium_data_attributes.fixtures import Dropdown
        from selenium_data_attributes.element import Button, Div

        # Import locators from file above
        from locators import MyPageLocators

        class NavbarDropdown(Dropdown):

            container = Div(*MyPageLocators.DROPDOWN_CONTAINER)


    page.py

    .. code-block:: python

        from selenium_data_attributes.page import Page
        from fixtures import NavbarDropdown
        from locators import MyPageLocators

        class MyWebPage(Page):

            def __init__(self, driver):

                self.driver = driver

                self.navbar_dropdown = NavbarDropdown(driver, *MyPageLocators.DROPDOWN)


    main.py

    .. code-block:: python

        from my_page.page import MyWebPage
        from selenium import webdriver

        # Instantiate webdriver
        wd = webdriver.Firefox()

        web_page = MyWebPage(wd)

        web_page.navbar_dropdown.expand()

    """

    # The user MUST override this attribute
    container = None


class DropdownMenu(Dropdown, DropdownMixin):
    """Dropdown menu object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="someClassId" class="someClass">Open Menu</a>
            <ul>
                <li>
                    <a href="/some/location">Nav Link 1</a>
                </li>
                <li>
                    <a href="/other/location">Nav Link 2</a>
                </li>
            </ul>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <a data-qa-id="dropdown-button" id="someClassId" class="someClass">Open Menu</a>
            <ul>
                <li>
                    <a data-qa-id="drop-link-1" href="/some/location">Nav Link 1</a>
                </li>
                <li>
                    <a data-qa-id="drop-link-2" href="/other/location">Nav Link 2</a>
                </li>
            </ul>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, //div[@data-qa-id="dropdown-button"])
            d = structures.DropdownMenu(driver, *locator)

            # Example usage:
            d.expand()
            d.select('link-2')
    """

    # The user MUST override this attribute
    container = None

    def select_by_index(self, index):
        """Click item within dropdown box

        :param int index: Item index
        :return: True, if the element is found and clicked
        :rtype: bool
        """

        if isinstance(index, int):
            index = str(index)

        elif isinstance(index, str):

            if index.isdigit():
                pass

            else:
                raise KeyError("Invalid argument for 'index'")

        else:
            KeyError("Invalid argument for 'index'")

        if isinstance(self.container, List):

            if self.container.exists():

                self.expand()
                item = self.container.get_by_index(index)

                if isinstance(item, Element):
                    item.click()
                    return True

        return False

    def select_by_value(self, value, selector):
        """Click item within dropdown box

        :param str value: Value to match
        :param str selector: Item to select
        :return: True, if the element is found and clicked
        :rtype: bool
        """

        if isinstance(self.container, List) and isinstance(value, str) and isinstance(selector, str):

            if self.container.exists():

                self.expand()
                item = self.container.get_by_value(value=value, selector=selector)

                if isinstance(item, Element):
                    item.click()
                    return True

        return False


class List(Element):
    """List object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <ul id="someList" class="someClass">
                <li>
                    <p id="name-0">John</p>
                    <p id="surname-0">Smith</p>
                    <p id="email-0">jsmith@somemail.net</p>
                </li>
                <li>
                    <p id="name-1">Jane</p>
                    <p id="surname-1">Doe</p>
                    <p id="email-1">djoe@trashmail.com</p>
                </li>
            </ul>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <ul data-qa-id="some-list" id="someList" class="someClass">
                <li>
                    <p data-qa-id="list-name[0]" id="name-0">John</p>
                    <p data-qa-id="list-surname[0]" id="surname-0">Smith</p>
                    <p data-qa-id="list-email[1]" id="email-0">jsmith@somemail.net</p>
                </li>
                <li>
                    <p data-qa-id="list-name[1]" id="name-1">Jane</p>
                    <p data-qa-id="list-surname[1]" id="surname-1">Doe</p>
                    <p data-qa-id="list-email[1]" id="email-1">djoe@trashmail.com</p>
                </li>
            </ul>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//ul[@data-qa-id="some-list"]")
            l = structures.List(driver, *locator)

            # Example usage. Returns "John":
            l[0].name

    """

    def __init__(self, web_driver, by=By.XPATH, path=None, _class=None, regex='.*', attrib='id', **kwargs):
        """List element. Includes ol and ul

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        super(List, self).__init__(web_driver=web_driver, by=by, path=path, **kwargs)

        self._class = _class if issubclass(_class, Element) else Element
        self._regex = regex if isinstance(regex, str) else ''
        self._attrib = attrib if isinstance(attrib, str) else 'id'

    def __len__(self):
        """Returns the number of associated elements

        :return: Number of associated elements
        :rtype: int
        """

        return len(self.items())

    def __getitem__(self, item):
        return self.get_by_index(item)

    def items(self):
        """Returns a list of associated elements

        :return: List of associated elements
        :rtype: list
        """

        if self.exists():
            return [self._class(self.driver, By.XPATH,
                                '//{0}[@{1}="{2}"]'.format(result.tag_name, self._attrib,
                                                           result.get_attribute(self._attrib).encode('ascii',
                                                                                                     'ignore')))
                    for result in self.driver.find_elements_by_xpath("//*[contains(@{0}, '{1}')]".format(self._attrib,
                                                                                                         self._regex))]

    def get_by_index(self, index):
        """Select item value from list by index i

        :param int index: Row of list
        :return: Value of selection at index
        :rtype: str
        """

        if isinstance(index, int) or isinstance(index, str):

            if isinstance(index, str):
                index = int(index) if index.isdigit() else 0

            return self.items()[index] if index in range(0, self.__len__()) else None

    def get_by_value(self, value, selector):
        """Select item value where values match

        :param str value: Value to match
        :param str selector: Item to return
        :return: Value of selection at index
        :rtype: str
        """

        if isinstance(value, str) and isinstance(selector, str):
            for item in self.items():
                return item if item.__getattr__(selector) == value else None


class Search(Element, InputMixin):
    """Search object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="search" class="someClass">
            <span class="closeButton" on-click="search.clear"><i class="closeIcon"></i></span>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.


        .. code-block:: html

            <input data-qa-id="search-identifier" id="someClassId" type="search" class="someClass">
            <span data-qa-id="search-clear" class="closeButton" on-click="search.clear"><i class="closeIcon"></i></span>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="search-identifier"]")
            s = structures.Search(driver, *locator)

            # Example usage:
            s.input('Hello World')

    """

    # The user MUST override this attribute
    clear = None


class SearchBox(Search, DropdownMixin):
    """Search box object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="search" class="someClass">
            <span class="closeButton" on-click="search.clear"><i class="closeIcon"></i></span>
            <div id="resultContainer" class="containerClass">
                <ul>
                    <li>
                        <a id="result-0" href="#">Search Result 1</a>
                    </li>
                    <li>
                        <a id="result-1" href="#">Search Result 2</a>
                    </li>
                    <li>
                        <a id="result-2" href="#">Search Result 2</a>
                    </li>
                </ul>
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.


        .. code-block:: html

            <input data-qa-id="search-identifier" id="someClassId" type="search" class="someClass">
            <span data-qa-id="search-clear" class="closeButton" on-click="search.clear"><i class="closeIcon"></i></span>
            <div id="resultContainer" class="containerClass">
                <ul>
                    <li>
                        <a data-qa-id="search-result[0]" id="result-0" href="#">Search Result 1</a>
                    </li>
                    <li>
                        <a data-qa-id="search-result[1]" id="result-1" href="#">Search Result 2</a>
                    </li>
                    <li>
                        <a data-qa-id="search-result[2]" id="result-2" href="#">Search Result 2</a>
                    </li>
                </ul>
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="search-identifier"]")
            s = structures.SearchBox(driver, *locator)

            s.input('Hello World')

    """

    # The user MUST override this attribute
    container = None


class TabNavigation(Element):
    """Tab navigation object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <nav id="someClassId" class="someClass">
                <ul>
                    <li>
                        <a href="/some/location">Nav Link 1</a>
                    </li>
                    <li>
                        <a href="/other/location">Nav Link 2</a>
                    </li>
                </ul>
            </nav>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <nav data-qa-id="nav-identifier" id="someClassId" class="someClass">
                <ul>
                    <li>
                        <a data-qa-id="nav-link-1" href="/some/location">Nav Link 1</a>
                    </li>
                    <li>
                        <a data-qa-id="nav-link-2" href="/other/location">Nav Link 2</a>
                    </li>
                </ul>
            </nav>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//nav[@data-qa-id="nav-identifier"]")
            n = structures.TabNavigation(driver, *locator)

            # Example usage
            n.select('link-2')
    """

    # You MUST define the links within the tab navigation yourself

    def links(self):
        """Returns all links in a navbar

        :return: Dictionary of WebElements
        :rtype: dict
        """

        return dict(inspect.getmembers(self, lambda attrib: not(inspect.isroutine(attrib)) and isinstance(attrib,
                                                                                                          Element)))

    def select(self, value):
        """Click item within navigation

        :param str value: id selector
        :return:
        """

        links = self.links()

        if str(value) in links.keys():
            if 'active' not in links[str(value)].cls:
                links[str(value)].click()
                return

    def selected(self):
        """Return a list of elements that are selected

        :return: List of WebElements
        :rtype: list
        """

        links = self.links()
        return [link for link in links.keys() if 'active' in links[link].cls]
