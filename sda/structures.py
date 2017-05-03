# -*- coding: utf-8 -*-
"""sda.structures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect
import sys
import warnings
from selenium.webdriver.common.by import By
from sda.element import *
from sda.mixins import *

__all__ = ['Button', 'Div', 'Image', 'InputCheckbox', 'InputRadio', 'InputText', 'Link', 'Select', 'Text']


class Button(Element, ClickMixin, TextMixin):
    """The Button implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <button id="someClassId" class="someClass" on-click="javascript.function" >Click Me</button>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <button data-qa-id="some-identifier" id="someClassId" class="someClass" on-click="javascript.function">
                Click Me
            </button>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some-identifier"]")
            b = structures.Button(driver, *locator)

            # Example usage
            b.click()
    """

    pass


class Div(Element):
    """The Div implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <div id="someClassId" class="someClass">
                ...
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <div data-qa-id="some-identifier" id="someClassId" class="someClass">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some-identifier"]")
            d = structures.Button(driver, *locator)

    """

    pass


class Dropdown(Element, ClickMixin, TextMixin):
    """The Dropdown implementation

    .. note:: This structure is specifically for a Bootstrap dropdown

    **Example Use:**

    .. code-block:: html

            <div class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example
                <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li><a href="#">HTML</a></li>
                    ...
                </ul>
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value as well as "data-qa-model" with a type.

        .. code-block:: html

            <div class="dropdown" data-qa-id="some.identifier" data-qa-model="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">Dropdown Example
                <span class="caret"></span></button>
                <ul class="dropdown-menu">
                    <li><a href="#">HTML</a></li>
                    ...
                </ul>
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            from selenium.webdriver import Chrome
            from sampyl import App

            wd = webdriver.Chrome('/path/to/chromedriver')
            app = App(wd, "http://someurl.com/path")

            # Opens the dropdown
            app.page.some.identifier.expand()

    """

    _toggle_xpath = (By.XPATH, '/descendant-or-self::*[(contains(@class, "dropdown-toggle") or '
                               '@ng-mouseover or @ng-click)]')

    @property
    def _container(self):
        """Dropdown container

        :return:
        """

        xpath = '/following-sibling::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'
        child = '/descendant-or-self::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'

        xpath_term = join(self.search_term, self._toggle, (By.XPATH, xpath))
        child_term = join(self.search_term, self._toggle, (By.XPATH, child))

        return Div(self.driver, By.XPATH, '|'.join([xpath_term[1], child_term[1]]))

    @property
    def _toggle(self):
        """Show/hide toggle button

        :return:
        """

        return Button(self.driver, *join(self.search_term, self._toggle_xpath))

    def expand(self, hover=False):
        """Show dropdown

        :return:
        """

        if not self._container.is_displayed():

            if hover:
                self._toggle.hover()
            else:
                self._toggle.click()

            return self._container.wait_until_appears()

    def collapse(self, hover=False):
        """Hide dropdown

        :return:
        """

        if self._container.is_displayed():

            if hover:
                self._toggle.hover()
            else:
                self._toggle.click()

            return self._container.wait_until_disappears()
class Image(Element):
    """The Image implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <img id="someClassId" class="someClass" />


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <img data-qa-id="some-identifier" id="someClassId" class="someClass" />


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//img[@data-qa-id="some-identifier"]")
            i = structures.Image(driver, *locator)

            # Returns tag attribute 'src'
            i.source()
    """

    def source(self):
        """Returns image source URL

        :return: Image source URL
        :rtype: str
        """

        return self.src


class InputCheckbox(Element, SelectiveMixin):
    """The InputCheckbox implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="checkbox" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="checkbox" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            c = structures.InputCheckbox(driver, *locator)

            # Example usage
            c.select()
    """

    def label(self):
        """Returns the label for the input item

        :return: Returns Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH, '//label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class InputRadio(InputCheckbox, SelectiveMixin):
    """The InputRadio implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="radio" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="radio" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            r = structures.InputRadio(driver, "//input[@data-qa-id="some-identifier"]")

            # Input Radio inherits from InputCheckbox
            r.select()
    """

    pass


class InputText(Element, InputMixin, ClickMixin):
    """The InputText implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="text" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some-identifier" id="someClassId" type="text" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            t = structures.InputText(driver, *locator)

            # Example usage
            t.input('Hello World')
    """

    def label(self):
        """Returns the label for the input item

        :return: Text object for label
        :rtype: Text
        """

        if self.exists():
            return Text(self.driver, By.XPATH, '//label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if len(self.id) > 0 else ''


class Link(Button, ClickMixin, TextMixin):
    """The Link implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <a data-qa-id="some-identifier" id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//a[@data-qa-id="some-identifier"]")
            l = structures.Link(driver, *locator)

            # Inherits from Button
            l.click()
    """

    pass


class Select(Element, SelectMixin):
    """The Select implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <select id="someClassId" class="someClass">
                <option value="1">Value 1</option>
                <option value="2">Value 2</option>
                <option value="3">Value 3</option>
                <option value="4">Value 4</option>
            </select>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <select data-qa-id="some-identifier" id="someClassId" class="someClass">
                <option value="1">Value 1</option>
                <option value="2">Value 2</option>
                <option value="3">Value 3</option>
                <option value="4">Value 4</option>
            </select>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            s = structures.Select(driver, *locator)

            # Example usage. Returns ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            s.options()
    """

    pass


class Text(Element, TextMixin, ClickMixin):
    """The Text implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <p id="someClassId" class="someClass">
                ...
            </p>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <p data-qa-id="some-identifier" id="someClassId" class="someClass">
                ...
            </p>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//p[@data-qa-id="some-identifier"]")
            d = structures.Text(driver, *locator)

            # Prints text inside text elements
            print d
    """

    pass
