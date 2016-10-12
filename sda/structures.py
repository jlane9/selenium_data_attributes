# -*- coding: utf-8 -*-
"""sda.structures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""


from selenium.webdriver.common.by import By

from element import *
from mixins import *

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.8'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Beta'
__docformat__ = 'reStructuredText'

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
