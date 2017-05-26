# -*- coding: utf-8 -*-
"""sda.structures

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

import inspect
import sys
import warnings
from selenium.webdriver.common.by import By
from sda.element import Element, join
from sda.mixins import ClickMixin, InputMixin, SelectMixin, SelectiveMixin, TextMixin, to_int

__all__ = ['Button', 'Div', 'Dropdown', 'Form', 'Image', 'InputCheckbox', 'InputRadio', 'InputText', 'Link',
           'MultiSelect', 'Select', 'Text']


class Button(Element, ClickMixin, TextMixin):
    """The Button implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <button id="someClassId" class="someClass" on-click="javascript.function" >Click Me</button>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <button data-qa-id="some.identifier" id="someClassId" class="someClass" on-click="javascript.function">
                Click Me
            </button>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some.identifier"]")
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

            <div data-qa-id="some.identifier" id="someClassId" class="someClass">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//button[@data-qa-id="some.identifier"]")
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

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some.identifier"]")
            d = structures.Dropdown(driver, *locator)

            # Example usage
            d.expand()

    """

    _toggle_xpath = (By.XPATH, '/descendant-or-self::*[(contains(@class, "dropdown-toggle") or '
                               '@ng-mouseover or @ng-click @on-click)]')

    @property
    def container(self):
        """Dropdown container

        :return:
        """

        xpath = '/following-sibling::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'
        child = '/descendant-or-self::*[(contains(@class, "dropdown-menu") or contains(@class, "tree") or @ng-show) ' \
                'and (self::div or self::ul)]'

        xpath_term = join(self.search_term, self.toggle, (By.XPATH, xpath))
        child_term = join(self.search_term, self.toggle, (By.XPATH, child))

        return Div(self.driver, By.XPATH, '|'.join([xpath_term[1], child_term[1]]))

    @property
    def toggle(self):
        """Show/hide toggle button

        :return:
        """

        return Button(self.driver, *join(self.search_term, self._toggle_xpath))

    def expand(self, hover=False):
        """Show dropdown

        :return:
        :rtype: bool
        """

        if not self.container.is_displayed():

            if hover:
                self.toggle.hover()

            else:
                self.toggle.click()

            return self.container.wait_until_appears()

        return False

    def collapse(self, hover=False):
        """Hide dropdown

        :return:
        :rtype: bool
        """

        if self.container.is_displayed():

            if hover:
                self.toggle.hover()

            else:
                self.toggle.click()

            return self.container.wait_until_disappears()

        return False


class Field(Element):
    """Field implementation
    """

    def label(self):
        """Returns the label for the input item

        :return: Field label
        :rtype: str
        """

        if self.exists():
            return Text(self.driver, By.XPATH, '//label[@for="{0}"]'.format(str(self.id))).visible_text() \
                if self.id else ''

        return ''


class Form(Element):
    """The Form implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <form id="someForm">
                <input id="someClassId" type="checkbox" class="someClass">
                ...
            </form>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <form id="someForm" data->
                <input id="someClassId" type="checkbox" class="someClass">
                ...
            </form>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some-identifier"]")
            form = structures.Form(driver, *locator)

            # Example usage
            field = form.get_field('someClassId')
    """

    def _get_field(self, field_name):
        """Returns field with id `field_name`

        :param basestring field_name: Form field to get
        :return:
        """

        if not isinstance(field_name, (str, unicode)):
            raise TypeError

        xpath = '/descendant-or-self::*[((self::input and @type="text") or ' \
                'self::textarea or self::select) and @name="{}"]'
        elements = self.driver.find_elements(*join(self.search_term, (By.XPATH, xpath.format(field_name))))

        if elements:
            return elements[0]

    def get_field(self, field_name):
        """Returns field with id `field_name`

        :param basestring field_name: Form field to get
        :return:
        """

        field = self._get_field(field_name)

        if field:

            input_xpath = '/descendant-or-self::*[((self::input and @type="text") or self::textarea) and @name="{}"]'
            select_xpath = '/descendant-or-self::*[self::select and @name="{}"]'

            if field.tag_name == u'input' or field.tag_name == u'textarea':
                return InputText(self.driver, *join(self.search_term, (By.XPATH, input_xpath.format(field_name))))

            elif field.tag_name == u'select':
                return Select(self.driver, *join(self.search_term, (By.XPATH, select_xpath.format(field_name))))

            else:
                warnings.warn('{} type not currently supported within form'.format(str(field.tag_name)))


class Image(Element):
    """The Image implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <img id="someClassId" class="someClass" />


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <img data-qa-id="some.identifier" id="someClassId" class="someClass" />


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//img[@data-qa-id="some.identifier"]")
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


class InputCheckbox(Field, SelectiveMixin):
    """The InputCheckbox implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="checkbox" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some.identifier" id="someClassId" type="checkbox" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some.identifier"]")
            c = structures.InputCheckbox(driver, *locator)

            # Example usage
            c.select()
    """

    pass


class InputRadio(InputCheckbox, SelectiveMixin):
    """The InputRadio implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="radio" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some.identifier" id="someClassId" type="radio" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            r = structures.InputRadio(driver, "//input[@data-qa-id="some.identifier"]")

            # Input Radio inherits from InputCheckbox
            r.select()
    """

    pass


class InputText(Field, InputMixin, ClickMixin):
    """The InputText implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <input id="someClassId" type="text" class="someClass">


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <input data-qa-id="some.identifier" id="someClassId" type="text" class="someClass">


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//input[@data-qa-id="some.identifier"]")
            t = structures.InputText(driver, *locator)

            # Example usage
            t.input('Hello World')
    """

    pass


class Link(Button, ClickMixin, TextMixin):
    """The Link implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <a data-qa-id="some.identifier" id="someClassId" class="someClass" href="/some/link/path">Click Me</a>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//a[@data-qa-id="some.identifier"]")
            l = structures.Link(driver, *locator)

            # Inherits from Button
            l.click()
    """

    pass


class MultiSelect(Element):
    """The MultiSelect implementation

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <div id="someClassId" class="someClass" isteven-multi-select input-model="some.model"
            output-model="format.model" helper-elements="filter all none">
                ...
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value as well as "data-qa-model" with a type.

        .. code-block:: html

            <div data-qa-id="some.identifier" data-qa-model="multiselect" id="someClassId" class="someClass"
            isteven-multi-select input-model="some.model" output-model="format.model" helper-elements="filter all none">
                ...
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//a[@data-qa-id="some.identifier"]")
            m = structures.MultiSelect(driver, *locator)

            # Example usage
            l.expand()

    """

    @property
    def _container(self):
        """iSteven dropdown container

        :return:
        """

        xpath = '/descendant-or-self::div[contains(@class, "checkboxLayer")]'

        return Div(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _toggle(self):
        """Show/hide button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "toggle")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _select_all(self):
        """Select all button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "all")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _select_none(self):
        """Select none button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "none")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _reset(self):
        """Reset button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "reset")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _filter(self):
        """Search field

        :return:
        """

        xpath = '/descendant-or-self::input[contains(@ng-click, "filter")]'

        return InputText(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    @property
    def _clear(self):
        """Clear search button

        :return:
        """

        xpath = '/descendant-or-self::button[contains(@ng-click, "clear")]'

        return Button(self.driver, *join(self.search_term, (By.XPATH, xpath)))

    def _get_index(self, idx):
        """Return item at index 'i'

        :param str idx: Index
        :return:
        """

        idx = to_int(idx)
        xpath = '/descendant-or-self::div[contains(@ng-repeat, "filteredModel")][{}]'

        if isinstance(idx, int):

            if idx in range(0, len(self.options())):
                return Button(self.driver, *join(self.search_term, (By.XPATH, xpath.format(idx))))

    def _get_text(self, text):
        """Return selection that contains text criteria

        :param str text: Text criteria
        :return:
        """

        xpath = '/descendant-or-self::label[contains(., "{}")]/ancestor::div[contains(@ng-repeat, "filteredModel")]'

        if isinstance(text, (str, unicode)):
            return Button(self.driver, *join(self.search_term, (By.XPATH, xpath.format(text))))

    def expand(self):
        """Show iSteven dropdown

        :return:
        :rtype: bool
        """

        if not self._container.is_displayed():

            self._toggle.click()
            return self._container.wait_until_appears()

        return False

    def collapse(self):
        """Hide iSteven dropdown

        :return:
        :rtype: bool
        """

        if self._container.is_displayed():

            self._toggle.click()
            return self._container.wait_until_disappears()

        return False

    def select_all(self):
        """Select all possible selections

        :return:
        :rtype: bool
        """

        self.expand()
        return self._select_all.click()

    def select_none(self):
        """Deselect all selections

        :return:
        :rtype: bool
        """

        self.expand()
        return self._select_none.click()

    def reset(self):
        """Reset selection to default state

        :return:
        :rtype: bool
        """

        self.expand()
        return self._reset.click()

    def search(self, value, clear=True):
        """Filter selections to those matching search criteria

        :param str value: Search criteria
        :param bool clear: Clear previous search criteria
        :return:
        :rtype: bool
        """

        self.expand()
        return self._filter.input(value, clear)

    def clear_search(self):
        """Click clear search button

        :return:
        :rtype: bool
        """

        self.expand()
        return self._clear.click()

    def select_by_index(self, index):
        """Select option at index 'i'

        :param str index: Index
        :return:
        :rtype: bool
        """

        self.expand()

        option = self._get_index(index)

        if option.exists() and 'selected' not in option.class_:
            return option.click()

        return False

    def select_by_text(self, text):
        """Select option that matches text criteria

        :param str text: Text criteria
        :return:
        :rtype: bool
        """

        self.expand()

        option = self._get_text(text)

        if option.exists() and 'selected' not in option.class_:
            option.click()

        return False

    def deselect_by_index(self, index):
        """Deselect option at index 'i'

        :param str index: Index
        :return:
        :rtype: bool
        """

        self.expand()

        option = self._get_index(index)

        if option.exists() and 'selected' in option.class_:
            option.click()

        return False

    def deselect_by_text(self, text):
        """Deselect option that matches text criteria

        :param str text: Text criteria
        :return:
        :rtype: bool
        """

        self.expand()

        option = self._get_text(text)

        if option.exists() and 'selected' in option.class_:
            option.click()

        return False

    def options(self, include_group=True):
        """Return all available options

        :param bool include_group: True, to include groupings
        :return: List of options
        :rtype: list
        """

        if include_group:
            xpath = '/descendant-or-self::div[contains(@ng-repeat, "filteredModel")]//label'

        else:
            xpath = '/descendant-or-self::div[contains(@ng-repeat, "filteredModel") and ' \
                    'not(contains(@class, "multiSelectGroup"))]//label'

        search_term = join(self.search_term, (By.XPATH, xpath))

        return [element.get_attribute('textContent').encode('ascii', 'ignore')
                for element in self.driver.find_elements(*search_term)]

    def selected_options(self):
        """Return all selected options

        :return: List of selected options
        :rtype: list
        """

        search_term = join(self.search_term, (By.XPATH, '/descendant-or-self::div[contains(@ng-repeat, '
                                                        '"filteredModel") and contains(@class, "selected")]//label'))

        return [element.get_attribute('textContent').encode('ascii', 'ignore')
                for element in self.driver.find_elements(*search_term)]


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

            <select data-qa-id="some.identifier" id="someClassId" class="someClass">
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

            locator = (By.XPATH, "//input[@data-qa-id="some.identifier"]")
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

            <p data-qa-id="some.identifier" id="someClassId" class="someClass">
                ...
            </p>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium.webdriver.common.by import By
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            locator = (By.XPATH, "//p[@data-qa-id="some.identifier"]")
            d = structures.Text(driver, *locator)

            # Prints text inside text elements
            print d
    """

    pass

MEMBERS = inspect.getmembers(sys.modules[__name__], predicate=lambda o: inspect.isclass(o) and issubclass(o, Element))
TYPES = {_type[0].lower(): _type[1] for _type in MEMBERS}
