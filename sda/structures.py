"""Structures

.. note::
    Some structures need specific keywords to find related elements. This means it is best practice to avoid using
    these keywords in your general naming conventions. See core module for more details.
    * cancel - Modal, Form and DropdownForm all use this keyword to find its cancel button
    * clear - Search and SearchBox both use this keyword to find its clear field button
    * close - Modal uses this keyword to find the close modal button
    * select-all - Table uses this to find a select-all checkbox in the header
    * submit - Modal, Form and DropdownForm all use this keyword to find its submit button
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select as SeleniumSelect
import re

from core import *
from element import *
from mixins import *

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.6.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Button', 'Div', 'Dropdown', 'DropdownForm', 'DropdownMenu', 'Form', 'Image', 'InputCheckbox', 'InputRadio',
           'InputText', 'Link', 'List', 'Modal', 'Search', 'SearchBox', 'Select', 'TabNavigation', 'Table', 'Text']


# --------------------------------------------------- Base Elements -------------------------------------------------- #
class Button(Element, ClickMixin, TextMixin):
    """Clickable object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            b = structures.Button(driver, "//button[@data-qa-id="some-identifier"]")

            # Example usage
            b.click()
    """

    pass


class Div(Element):
    """Container object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            d = structures.Div(driver, "//div[@data-qa-id="some-identifier"]")
    """

    pass


class Image(Element):
    """Image object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            i = structures.Image(driver, "//img[@data-qa-id="some-identifier"]")

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
    """Input checkbox object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            c = structures.InputCheckbox(driver, "//input[@data-qa-id="some-identifier"]")

            # Example usage
            c.select()
    """

    def __init__(self, web_driver, path, identifier=DEFAULT_IDENTIFIER):

        Element.__init__(self, web_driver, path, identifier=identifier)

        if self.id:

            self.label = Text(web_driver, '//label[@for="{0}"]'.format(str(self.id)))
            return

        self.label = ''


class InputRadio(InputCheckbox, SelectiveMixin):
    """Input radio object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            r = structures.InputRadio(driver, "//input[@data-qa-id="some-identifier"]")

            # Input Radio inherits from InputCheckbox
            r.select()
    """

    pass


class InputText(Element, InputMixin):
    """Input text object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            t = structures.InputText(driver, "//input[@data-qa-id="some-identifier"]")

            # Example usage
            t.input('Hello World')
    """

    pass


class Link(Button, ClickMixin, TextMixin):
    """Link object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            l = structures.Link(driver, "//a[@data-qa-id="some-identifier"]")

            # Inherits from Button
            l.click()
    """

    pass


class Select(Element, SelectMixin):
    """Select object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            s = structures.Select(driver, "//input[@data-qa-id="some-identifier"]")

            # Example usage. Returns ['Value 1', 'Value 2', 'Value 3', 'Value 4']
            s.options()
    """

    pass


class Text(Element, TextMixin):
    """Text object

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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            d = structures.Text(driver, "//p[@data-qa-id="some-identifier"]")

            # Prints text inside text elements
            print d
    """

    pass


# --------------------------------------------------- Simple Structures ---------------------------------------------- #
class Dropdown(Element, DropdownMixin):
    """Abstract class for dropdown elements
    """

    def __init__(self, web_driver, path, dropdown_path=None, identifier=DEFAULT_IDENTIFIER):
        """Dropdown element

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, web_driver, path, identifier=identifier)

        if isinstance(dropdown_path, str):

            if len(dropdown_path) > 0:

                self.container = List(web_driver, dropdown_path)
                return

        self.container = List(web_driver, '{0}/following-sibling::*[self::ul or self::ol or self::div]'.format(path))


class Form(Element):
    """Form object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html
        
            <form id="sampleForm">
                <input id="inputField" class="someClass" type="text">
                <button id="cancelButton" class="btn btn-primary">Cancel</button>
                <button id="submitButton" class="btn btn-primary">Submit</button>
            </form>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <form data-qa-id="sample-form" id="sampleForm">
                <input data-qa-id="form-field-1" id="inputField" class="someClass" type="text">
                <button data-qa-id="form-cancel" id="cancelButton" class="btn btn-primary">Cancel</button>
                <button data-qa-id="form-submit" id="submitButton" class="btn btn-primary">Submit</button>
            </form>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            f = structures.Form(driver, "//form[@data-qa-id="sample-form"]")

            # Example usage:
            f['field-1'] = "Hello World"
            f.submit()
    """

    def __init__(self, web_driver, path, identifier=DEFAULT_IDENTIFIER):
        """

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :param str identifier: Tag identifier
        :return:
        """

        Element.__init__(self, web_driver, path, identifier=identifier)

        self._submit = Button(web_driver, '{0}//*[contains(@{1}, "{2}")]'.format(path, self._identifier,
                                                                                 SUBMIT_IDENTIFIER))
        self._cancel = Button(web_driver, '{0}//*[contains(@{1}, "{2}")]'.format(path, self._identifier,
                                                                                 CANCEL_IDENTIFIER))

    @encode_ascii()
    def __getitem__(self, instance):
        """Get (value) for field instance

        :param str instance: id selector
        :return:
        """

        if self.exists():

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, "{2}")]'.format(self.search_term[1],
                                                                                                 self._identifier,
                                                                                                 str(instance)))

            # Get the first element that contains (instance) in the data-qa-id
            if len(elements) > 0:
                return elements[0].get_attribute('value')

            else:
                error = 'Form field {0} cannot be found.'.format(str(instance))
                raise NoSuchElementException(error)

        else:
            raise NoSuchElementException('Form cannot be found.')

    def __setitem__(self, instance, value):
        """Input (value) for field (instance)

        :param str instance: id selector
        :param str value: Value to set
        :return:
        """

        if self.exists():

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, "{2}")]'.format(self.search_term[1],
                                                                                                 self._identifier,
                                                                                                 str(instance)))

            # Click the first element that contains (instance) in the data-qa-id
            if len(elements) > 0:

                tag_name = elements[0].tag_name.encode('ascii', 'ignore')

                if tag_name == 'select':

                    select = SeleniumSelect(elements[0])
                    select.select_by_visible_text(str(value))

                elif tag_name == 'input':

                    input_type = elements[0].get_attribute('type').encode('ascii', 'ignore')

                    if input_type in ['button', 'reset', 'submit']:
                        elements[0].click()

                    elif input_type in ['checkbox', 'radio']:

                        # User would use True if they want to assign
                        if value:
                            if not elements[0].is_selected():
                                elements[0].click()

                        # User would use False if the want to un-assign
                        else:
                            if elements[0].is_selected():
                                elements[0].click()

                    else:

                        elements[0].clear()
                        elements[0].send_keys(str(value))

                elif tag_name == "textarea":
                    elements[0].clear()
                    elements[0].send_keys(str(value))

                else:

                    if value:
                        elements[0].click()

            else:
                error = 'Form field {0} cannot be found.'.format(str(instance))
                raise NoSuchElementException(error)

        else:
            raise NoSuchElementException('Form cannot be found.')

    def submit(self):
        """Submit form

        :return:
        """

        self._submit.click()

    def cancel(self):
        """Cancel form

        :return:
        """

        self._cancel.click()

    def fields(self):
        """Returns all available fields for this form

        :return:
        """

        if self.exists():
            return self.driver.find_elements_by_xpath('{0}//*[@{1}] and (self::input or self::textarea or self::button '
                                                      'or self::select)'.format(self.search_term[1]), self._identifier)

    def field(self, instance):
        """Returns the field that matches the id selector

        :param str instance: id selector
        :return:
        :rtype: WebElement
        """

        if self.exists():

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, "{2}")]'.format(self.search_term[1],
                                                                                                 self._identifier,
                                                                                                 str(instance)))

            if len(elements) > 0:
                return elements[0]

            else:
                raise NoSuchElementException('Cannot find element')

        else:
            raise NoSuchElementException('Form cannot be found.')


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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            l = structures.List(driver, "//ul[@data-qa-id="some-list"]")

            # Example usage. Returns "John":
            l[0]['name'].get_attribute('textContent')
    """

    def __init__(self, web_driver, path, identifier=DEFAULT_IDENTIFIER):
        """List element. Includes ol and ul

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, web_driver, path, identifier=identifier)

    def __len__(self):
        """Returns the number of associated elements

        :return: Number of associated elements
        :rtype: int
        """

        return len(self.items())

    def __getitem__(self, key):

        output = self.items()

        try:

            if isinstance(key, int):
                return output[key]

        except IndexError:
            pass

        return []

    def items(self):
        """Returns a list of associated elements

        :return: List of associated elements
        :rtype: list
        """

        if self.exists():

            list_results = {}
            results = self.driver.find_elements_by_xpath('{0}//*[@{1}]'.format(self.search_term[1], self._identifier))

            # Build a dictionary with all result types tied to its index
            for result in results:

                r = re.findall(r'-([\w\d]+)\[(\d+)\]', result.get_attribute(self._identifier).encode('ascii', 'ignore'))

                if len(r) > 0:

                    result_type = r[0][0]
                    result_index = r[0][1]

                    if result_index.isdigit():

                        if result_index in list_results.keys():
                            list_results[result_index][result_type] = result

                        else:
                            list_results[result_index] = {result_type: result}

            # Recreate list_results as list
            return [list_results[index] for index in sorted(list_results.keys(), key=int)]

        return []

    def select_by_index(self, index, selector):
        """Select item value from list by index i

        :param int index: Row of list
        :param str selector: Item to return
        :return: Value of selection at index
        :rtype: str
        """

        if (isinstance(index, int) or isinstance(index, str)) and isinstance(selector, str):

            if isinstance(index, str):
                if index.isdigit():
                    index = int(index)

            if index in range(0, self.__len__()):

                item = self.items()[index]

                if selector in item.keys():
                    item[selector].click()
                    return

    def select_by_value(self, value, selector):
        """Select item value where values match

        :param str value: Value to match
        :param str selector: Item to return
        :return: Value of selection at index
        :rtype: str
        """

        if isinstance(value, str) and isinstance(selector, str):

            for row in self.items():

                values = [item.get_attribute('textContent').encode('ascii', 'ignore').strip().lower()
                          for item in row.values()]

                if value.lower() in values:
                    if selector in row.keys():
                        row[selector].click()
                        return


class Modal(Form):
    """Modal object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <div id="modalId" class="modalClass">
                <div class="modal-content">
                    <div class="modal-header">
                        Delete this person
                    </div>
                    <div class="modal-body">
                        Are you sure you what to delete? Enter the name of the person below to delete
                        <input id="someId" class="inputClass" type="text">
                    </div>
                    <div class="modal-footer">
                        <a href="#" on-click="close.Modal" class="cancelClass">Cancel</a>
                        <a href="#" on-click="submit.Modal" class="submitClass">Submit</a>
                    </div>
                </div>
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <div data-qa-id="sample-modal" id="modalId" class="modalClass">
                <div class="modal-content">
                    <div class="modal-header">
                        Delete this person
                    </div>
                    <div class="modal-body">
                        Are you sure you what to delete? Enter the name of the person below to delete
                        <input data-qa-id="delete-field" id="someId" class="inputClass" type="text">
                    </div>
                    <div class="modal-footer">
                        <a data-qa-id="modal-cancel" href="#" on-click="close.Modal" class="cancelClass">Cancel</a>
                        <a data-qa-id="modal-submit" href="#" on-click="submit.Modal" class="submitClass">Submit</a>
                    </div>
                </div>
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            f = structures.Modal(driver, "//div[@data-qa-id="sample-modal"]")

            # Example usage:
            f['field'] = "John Dow"
            f.submit()
    """

    def __init__(self, web_driver, path, identifier=DEFAULT_IDENTIFIER):
        """

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Form.__init__(self, web_driver, path, identifier=identifier)

        self._close = Button(web_driver, '{0}//*[contains(@{1}, "{2}")]'.format(path, self._identifier,
                                                                                CLOSE_IDENTIFIER))

    def close(self):
        """Close modal

        :return:
        """

        self._close.click()


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
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            s = structures.Search(driver, "//input[@data-qa-id="search-identifier"]")

            # Example usage:
            s.results.search('Hello World')
    """

    def __init__(self, web_driver, path, clear_path=None, identifier=DEFAULT_IDENTIFIER):
        """Search input element

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, web_driver, path, identifier=identifier)

        if isinstance(clear_path, str):

            if len(clear_path) > 0:

                self._clear = Button(web_driver, '{0}'.format(clear_path))
                return

        self._clear = Button(web_driver, '{0}/following-sibling::*[contains(@{1}, '
                                         '"{2}")]'.format(path, self._identifier, CLEAR_IDENTIFIER))

    def clear(self):
        """Clear search

        :return:
        """

        self._clear.click()

    def search(self, criteria):
        """Input criteria into input field

        :param str criteria: Search criteria
        :return:
        """

        self.input(str(criteria))


class Table(Element):
    """Table object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <table id="sampleTable">
                <thead>
                    <tr>
                        <th>Column 1</th>
                        <th>Column 2</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Jane</td>
                        <td>Doe</td>
                    </tr>
                    <tr>
                        <td>John</td>
                        <td>Smith</td>
                    </tr>
                </tbody>
            </table>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <table data-qa-id="sample-table" id="sampleTable">
                <thead>
                    <tr>
                        <th data-qa-id="column1">Column 1</th>
                        <th data-qa-id="column2">Column 2</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td data-qa-id="column1[0]">Jane</td>
                        <td data-qa-id="column2[0]">Doe</td>
                    </tr>
                    <tr>
                        <td data-qa-id="column1[1]">John</td>
                        <td data-qa-id="column2[1]">Smith</td>
                    </tr>
                </tbody>
            </table>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            t = structures.Table(driver, "//form[@data-qa-id="sample-table"]")

            # Example usage:
            t.headers = ['Column 1', 'Column 2']
    """

    ORDERS = (ASC_IDENTIFIER, DESC_IDENTIFIER, 'none')

    def __init__(self, web_driver, path, identifier=DEFAULT_IDENTIFIER):
        """

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, web_driver, path, identifier=identifier)
        self._rows = List(web_driver, '{0}//tbody'.format(path))

    def __len__(self):
        return len(self.rows())

    def __getitem__(self, key):
        return self._rows.__getitem__(key)

    @property
    def headers(self):
        """Return a list of table headers

        :return: List of table headers
        :rtype: list
        """

        if self.exists():

            element = self.element()

            return [i.get_attribute('textContent').encode('ascii', 'ignore')
                    for i in element.find_elements_by_xpath('.//th[@{0}]'.format(self._identifier))]

        return []

    @property
    def filter(self):
        """Return the web element for the current filtered header

        :return:
        """

        filters = self.driver.find_elements_by_xpath('{0}//*[not(contains(@class, "ng-hide")) and '
                                                     '(contains(@{1}, "{2}") or '
                                                     'contains(@{1}, "{3}"))]'.format(self.search_term[1],
                                                                                      self._identifier,
                                                                                      ASC_IDENTIFIER, DESC_IDENTIFIER))

        if len(filters) > 0:

            column = filters[0].find_element_by_xpath('.//ancestor::th')

            if ASC_IDENTIFIER in filters[0].get_attribute(self._identifier):
                return column, ASC_IDENTIFIER

            elif DESC_IDENTIFIER in filters[0].get_attribute(self._identifier):
                return column, DESC_IDENTIFIER

            else:
                return column, 'none'

        return None

    @filter.setter
    def filter(self, (value, order)):
        """Set the current filter to value in order specified

        :param value: Header id
        :param order: 'asc' or 'desc'
        :return:
        """

        if isinstance(order, str):

            if order.lower() in self.ORDERS:

                f = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, "{2}")]'.format(self.search_term[1],
                                                                                              self._identifier, value))

                if len(f) > 0:

                    button = Button(self.driver, '{0}//*[contains(@{1}, "{2}")]//*[(self::button or self::a or '
                                                 'self::input) or @ng-click]'.format(self.search_term[1],
                                                                                     self._identifier, value))

                    # If the current filter is already set to the filter specified
                    if f[0].get_attribute('textContent') == self.filter[0].get_attribute('textContent'):

                        # If the current filter already has the specified order
                        if order == self.filter[1]:
                            return

                        # If the current filter does not have the specified order
                        else:

                            while self.filter[1] != order:
                                button.click()
                                button.wait_until_present()

                    # If the current filter is not set to the specified filter
                    else:

                        button.click()
                        button.wait_until_present()

                        # If the current filter already has the specified order
                        if order == self.filter[1]:
                            return

                        # If the current filter does not have the specified order
                        else:

                            while self.filter[1] != order:
                                button.click()
                                button.wait_until_present()

    def filters(self):
        """Return a list of all available filters

        :return: Filters
        :rtype: list
        """

        return self.driver.find_elements_by_xpath('//*[contains(@{0}, "{1}") or '
                                                  'contains(@{0}, "{2}")]/ancestor::th'.format(self._identifier,
                                                                                               ASC_IDENTIFIER,
                                                                                               DESC_IDENTIFIER))

    def rows(self):
        """Returns a list of associated elements

        :return: List of associated elements
        :rtype: list
        """
        return self._rows.items()

    def select_all(self):
        """Click select all checkbox in header

        :return:
        """

        if self.exists():
            select_all = self.element().find_elements_by_xpath('.//th[contains(@{0}, '
                                                               '"{1}")]//input'.format(self._identifier,
                                                                                       SELECT_ALL_IDENTIFIER))

            if len(select_all) > 0:
                select_all[0].click()

            else:
                raise NoSuchElementException('Select all option not found.')

        else:
            NoSuchElementException('Table not found.')

    def select_by_index(self, index, selector):
        """Select item value from table by index i

        :param int index: Row of table
        :param str selector: Item to return
        :return: Value of selection at index
        :rtype: str
        """

        self._rows.select_by_index(index, selector)

    def select_by_value(self, value, selector):
        """Select item value where values match

        :param str value: Value to match
        :param str selector: Item to return
        :return: Value of selection at index
        :rtype: str
        """

        self._rows.select_by_value(value, selector)


# -------------------------------------------------- Complex Structures ---------------------------------------------- #
class DropdownForm(Dropdown, DropdownMixin):
    """Dropdown form object

        **Example Use:**


        Let's take the following example:

        .. code-block:: html

            <a id="dropdownOpen" class="someClass">Open Menu</a>
            <div>
                <form id="sampleForm">
                    <input id="inputField" class="someClass" type="text">
                    <button id="cancelButton" class="btn btn-primary">Cancel</button>
                    <button id="submitButton" class="btn btn-primary">Submit</button>
                </form>
            </div>


        If the user wants to make the code above recognizable to the testing framework, they would add the attribute
        "data-qa-id" with a unique value.

        .. code-block:: html

            <a data-qa-id="open-dropdown" id="dropdownOpen" class="someClass">Open Menu</a>
            <div>
                <form data-qa-id="sample-form" id="sampleForm">
                    <input data-qa-id="form-field-1" id="inputField" class="someClass" type="text">
                    <button data-qa-id="form-cancel" id="cancelButton" class="btn btn-primary">Cancel</button>
                    <button data-qa-id="form-submit" id="submitButton" class="btn btn-primary">Submit</button>
                </form>
            </div>


        An example on how to interact with the element:

        .. code-block:: python

            import selenium
            from selenium_data_attributes import structures

            driver = webdriver.FireFox()
            driver.get('http://www.some-url.com')

            f = structures.DropdownForm(driver, "//a[@data-qa-id="open-dropdown"]")

            # Example usage:
            f.expand()
            f['field-1'] = "Hello World"
            f.submit()
    """

    def __init__(self, web_driver, path, dropdown_path=None, identifier=DEFAULT_IDENTIFIER):
        """Dropdown form element

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Dropdown.__init__(self, web_driver, path, dropdown_path, identifier=identifier)

        if isinstance(dropdown_path, str):

            if len(dropdown_path) > 0:

                self.form = Form(web_driver, '{0}//form[@{1}]'.format(dropdown_path, self._identifier))
                return

        self.form = Form(web_driver, '{0}/following-sibling::*[self::div or self::ul or self::ol]'
                                     '//form[@{1}]'.format(path, self._identifier))

    def __getitem__(self, instance):
        """Get (value) for field instance

        :param instance:
        :return:
        """

        self.expand()
        self.form.__getitem__(instance)

    def __setitem__(self, instance, value):
        """Input (value) for field (instance)

        :param instance: Field ID
        :param value: Value to set
        :return:
        """

        self.expand()
        self.form.__setitem__(instance, value)

    def submit(self):
        """Submit form

        :return:
        """

        self.expand()
        self.form.submit()

    def cancel(self):
        """Cancel form

        :return:
        """

        self.expand()
        self.form.cancel()

    def fields(self):
        """Returns all available fields for this form

        :return: list of WebElements
        :rtype: list
        """

        return self.form.fields()

    def field(self, instance):
        """Return field that matches 'instance' in id

        :param str instance: Element id
        :return:
        """

        return self.form.field(instance)


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

            d = structures.DropdownMenu(driver, "//div[@data-qa-id="dropdown-button"]")

            # Example usage:
            d.expand()
            d.select('link-2')
    """

    def select(self, value):
        """Click item within dropdown box

        :param str value: id selector
        :return:
        """

        if self.container.exists():

            self.expand()

            # Find all items that we can select (click)
            items = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, '
                                                       '"{2}")]'.format(self.dropdown_list.search_term[1],
                                                                        self._identifier, value))

            if len(items) > 0:
                items[0].click()

            else:
                error = 'Dropdown item {0} cannot be found.'.format(str(value))
                raise NoSuchElementException(error)


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

            s = structures.SearchBox(driver, "//input[@data-qa-id="search-identifier"]")

            # Example usage. This will return {'result': <webelement>}:
            s.results.search('Hello World')
            s.results[0]
    """

    def __init__(self, web_driver, path, result_path=None, identifier=DEFAULT_IDENTIFIER):
        """

        :param WebDriver web_driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Search.__init__(self, web_driver, path, identifier=identifier)

        if isinstance(result_path, str):

            if len(result_path) > 0:

                self.container = List(web_driver, result_path)
                return

        self.container = List(web_driver, '{0}/following-sibling::*[self::ul or self::ol or self::div]'.format(path))


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

            n = structures.TabNavigation(driver, "//nav[@data-qa-id="nav-identifier"]")

            # Example usage
            n.select('link-2')
    """

    def select(self, value):
        """Click item within navigation

        :param str value: id selector
        :return:
        """

        if self.exists():

            # Find all items that we can select (click)
            items = self.driver.find_elements_by_xpath('{0}//*[contains(@{1}, '
                                                       '"{2}")]'.format(self.search_term[1], self._identifier, value))

            if len(items) > 0:
                items[0].click()

            else:
                error = 'Nav Bar item {0} cannot be found.'.format(str(value))
                raise NoSuchElementException(error)

        else:
            raise NoSuchElementException('Nav cannot be found.')

    def selected(self):
        """Return a list of elements that are selected

        :return: List of WebElements
        :rtype: list
        """

        output = list()

        if self.exists():

            selector = '//*[(self::a or self::input or self::button) and @{0}] ' \
                       'and contains(@class, "active")'.format(self._identifier)

            # Find all items that we can select (click)
            items = self.driver.find_elements_by_xpath('{0}{1}'.format(self.search_term[1], selector))

            for item in items:
                if item.is_selected():
                    output.append(item)

        return output
