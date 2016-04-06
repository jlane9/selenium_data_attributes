"""
    selenium_data_attributes.structures
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements objects that provide easier ways to interact with common web elements

    :copyright: (c) 2016 FanThreeSixty
    :author: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE for more details.

    .. note::
        Some structures need specific keywords to find related elements. This means it is best practice to avoid using
        these keywords in your naming conventions.
            * cancel - Modal, Form and DropdownForm all use this keyword to find its cancel button
            * clear - Search and SearchBox both use this keyword to find its clear field button
            * close - Modal uses this keyword to find the close modal button
            * select-all - Table uses this to find a select-all checkbox in the header
            * submit - Modal, Form and DropdownForm all use this keyword to find its submit button
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select as SeleniumSelect
import re

from element import *

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.3.2'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['Button', 'Div', 'Dropdown', 'DropdownForm', 'DropdownMenu', 'Form', 'Image', 'InputCheckbox', 'InputRadio',
           'InputText', 'Link', 'List', 'Modal', 'Search', 'SearchBox', 'Select', 'TabNavigation', 'Table', 'Text']


# ---------------------------------------------------- Base Structures ------------------------------------------------#
class Field(Element):
    """Abstract class for input elements
    """

    def __str__(self):
        return self.__getattr__('value')

    def __unicode__(self):
        return self.__getattr__('value')

    def is_disabled(self):
        """Returns True, if the button is disabled

        :return: True, if the button is disabled
        :rtype: bool
        """

        return self.__contains__('disabled')


# --------------------------------------------------- Simple Structures -----------------------------------------------#
class Button(Field):
    """
        Clickable object
        ~~~~~~~~~~~~~~~~

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

    def __str__(self):
        return self._text()

    def __unicode__(self):
        return self._text()

    def click(self):
        """Click button

        :return:
        """

        return self._click()


class Div(Element):
    """
        Container object
        ~~~~~~~~~~~~~~~~

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


class Dropdown(Element):
    """Abstract class for dropdown elements
    """

    def __init__(self, driver, path, dropdown_path=None):
        """Dropdown element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, path)

        if isinstance(dropdown_path, str):
            if len(dropdown_path) > 0:
                self.dropdown_list = List(driver, '{0}'.format(dropdown_path))
                return

        self.dropdown_list = List(driver, '{0}/following-sibling::*[self::ul or self::ol or self::div]'.format(path))

    def collapse(self):
        """Close dropdown

        :return:
        """

        if self.exists():
            if not self.dropdown_list.angular_hidden():
                self._click()

    def expand(self):
        """Expand dropdown

        :return:
        """

        if self.exists():
            if self.dropdown_list.angular_hidden():
                self._click()


class Form(Element):
    """
        Form object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, path)

        self._submit = Button(driver, '{0}//*[contains(@data-qa-id, "submit")]'.format(path))
        self._cancel = Button(driver, '{0}//*[contains(@data-qa-id, "cancel")]'.format(path))

    def __getitem__(self, instance):
        """Get (value) for field instance

        :param str instance: id selector
        :return:
        """

        if self.exists():

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                          '"{1}")]'.format(self.search_term[1], str(instance)))

            # Get the first element that contains (instance) in the data-qa-id
            if len(elements) > 0:
                return elements[0].get_attribute('value').encode('ascii', 'ignore')

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

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                          '"{1}")]'.format(self.search_term[1], str(instance)))

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
            return self.driver.find_elements_by_xpath('{0}//*[@data-qa-id] and (self::input or self::textarea or '
                                                      'self::button or self::select)'.format(self.search_term[1]))

    def field(self, instance):
        """Returns the field that matches the id selector

        :param str instance: id selector
        :return:
        :rtype: WebElement
        """

        if self.exists():

            elements = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                          '"{1}")]'.format(self.search_term[1], str(instance)))

            if len(elements) > 0:
                return elements[0]

            else:
                raise NoSuchElementException('Cannot find element')

        else:
            raise NoSuchElementException('Form cannot be found.')


class Image(Element):
    """
        Image object
        ~~~~~~~~~~~~~~~~

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

    pass


class InputCheckbox(Element):
    """
        Input Checkbox object
        ~~~~~~~~~~~~~~~~

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

    def deselect(self):
        """Deselect this element

        :return:
        """

        if self.selected():
            self._click()

    def label(self):
        """Returns the associated label if the element has one

        :return: Checkbox label
        :rtype: str
        """

        element_id = self.id

        if element_id != '':
            label_element = self.driver.find_elements_by_xpath('//label[@for="{0}"]'.format(element_id))

            if len(label_element) > 0:
                return label_element[0].get_attribute('textContent').encode('ascii', 'ignore')

        return ''

    def select(self):
        """Select this element

        :return:
        """

        if not self.selected():
            self._click()

    def selected(self):
        """Returns True, if the element is selected

        :return:
        """

        return self._selected()


class InputRadio(InputCheckbox):
    """
        Input Radio object
        ~~~~~~~~~~~~~~~~

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


class InputText(Field):
    """
        Input Text object
        ~~~~~~~~~~~~~~~~

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

    def input(self, text, clear=True):
        """Assign 'text' as input's value

        :param str text: Text value
        :param bool clear: True, to clear element of previous value
        :return:
        """

        self._input(text, clear)


class Link(Button):
    """
        Link object
        ~~~~~~~~~~~~~~~~

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


class List(Element):
    """
        List object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """List element. Includes ol and ul

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, path)

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
            results = self.driver.find_elements_by_xpath('{0}//*[@data-qa-id]'.format(self.search_term[1]))

            # Build a dictionary with all result types tied to its index
            for result in results:

                r = re.findall(r'-([\w\d]+)\[(\d+)\]', result.get_attribute('data-qa-id').encode('ascii', 'ignore'))

                if len(r) > 0:

                    result_type = r[0][0]
                    result_index = r[0][1]

                    if isinstance(result_index, str):

                        if result_index.isdigit():

                            if result_index in list_results:
                                list_results[int(result_index)][result_type] = result

                            else:
                                list_results[int(result_index)] = {result_type: result}

            # Recreate list_results as list
            list_indexes = list_results.keys()
            list_indexes.sort()

            return [list_results[item] for item in list_indexes]

    def select_by_index(self, index, selector):

        if isinstance(index, int) and isinstance(selector, str):

            if index in range(0, self.__len__()):

                item = self.items()[index]

                if selector in item.keys():
                    item[selector].click()
                    return

        elif isinstance(index, str) and isinstance(selector, str):

            if index.isdigit():

                if int(index) in range(0, self.__len__()):

                    item = self.items()[int(index)]

                    if selector in item.keys():
                        item[selector].click()
                        return

    def select_by_value(self, value, selector):

        if isinstance(value, str) and isinstance(selector, str):

            for row in self.items():

                values = [item.get_attribute('textContent').encode('ascii', 'ignore').strip().lower()
                          for item in row.values()]

                if value.lower() in values:
                    if selector in row.keys():
                        row[selector].click()
                        return


class Modal(Form):
    """
        Modal object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Form.__init__(self, driver, path)
        self._close = Button(driver, '{0}//*[contains(@data-qa-id, "close")]'.format(path))

    def close(self):
        """Close modal

        :return:
        """

        self._close.click()


class Search(Element):
    """
        Search object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """Search input element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, path)
        self._clear = Button(driver, '{0}/following-sibling::*[contains(@data-qa-id, "clear")]'.format(path))

    def clear(self):
        """Clear search

        :return:
        """

        self._clear._click()

    def search(self, criteria):
        """Input criteria into input field

        :param str criteria: Search criteria
        :return:
        """

        self._input(str(criteria))


class Select(Field):
    """
        Select object
        ~~~~~~~~~~~~~~~~

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

    @property
    def options(self):
        """Return select options

        :return:
        """

        return self._options()

    @property
    def selected(self):
        """Return which options are selected

        :return:
        """

        return self._selected_options()

    @property
    def selected_first(self):
        """Returns the first selected option

        :return:
        """

        return self._selected_first()

    def select(self, option):
        """Select an option

        :param option: Visible text, index or value
        :return: True, if option is selected
        :rtype: bool
        """

        if isinstance(option, str):

            result = self._select_by_text(option=option)

            if not result:
                return self._select_by_value(option=option)

            else:
                return result

        elif isinstance(option, int):
            return self._select_by_index(option=option)

        return False

    def deselect(self, option):
        """Deselect an option

        :param option: Visible text, index or value
        :return: True, if option is deselected
        :rtype: bool
        """

        if isinstance(option, str):

            result = self._deselect_by_text(option=option)

            if not result:
                return self._deselect_by_value(option=option)

            else:
                return result

        elif isinstance(option, int):
            return self._deselect_by_index(option=option)

        return False

    def deselect_all(self):
        """Deselect all options

        :return: True, if options are deselected
        :rtype: bool
        """

        return self._deselect_all()


class Table(Element):
    """
        Table object
        ~~~~~~~~~~~~~~~~

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

    ORDERS = ('asc', 'desc', 'none')

    def __init__(self, driver, path):
        """

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, path)
        self._rows = List(driver, '{0}//tbody'.format(path))

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

        element = self.element()

        if element:
            return [i.get_attribute('textContent').encode('ascii', 'ignore')
                    for i in element.find_elements_by_xpath('.//th[@data-qa-id]')]

        return []

    @property
    def filter(self):
        """Return the web element for the current filtered header

        :return:
        """

        filters = self.driver.find_elements_by_xpath('//*[(contains(@data-qa-id, "asc") or '
                                                     'contains(@data-qa-id, "desc")) and '
                                                     'not(contains(@class, "ng-hide"))]/ancestor::th')

        if len(filters) > 0:
            if 'asc' in filters[0].get_attribute('data-qa-id'):
                return filters[0], 'asc'

            elif 'desc' in filters[0].get_attribute('data-qa-id'):
                return filters[0], 'desc'

            else:
                return filters[0], 'none'

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

                f = self.driver.find_elements_by_xpath('{0}//*[(contains(@data-qa-id, '
                                                       '"{1}")]'.format(self.search_term[1], value))

                if len(f) > 0:

                    button = Button(self.driver, '{0}//*[(contains(@data-qa-id, "{1}")]//*[(self::button or self::a or '
                                                 'self::input) or @ng-click]'.format(self.search_term[1], value))

                    # If the current filter is already set to the filter specified
                    if f.get_attribute('textContent') == self.filter[0].get_attribute('textContent'):

                        # If the current filter already has the specified order
                        if order == self.filter[1]:
                            pass

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
                            button.click()

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

        return self.driver.find_elements_by_xpath('//*[contains(@data-qa-id, "asc") or '
                                                  'contains(@data-qa-id, "desc")]/ancestor::th')

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
            select_all = self.element().find_elements_by_xpath('.//th[contains(@data-qa-id, "select-all")]//input')

            if len(select_all) > 0:
                select_all[0].click()

            else:
                raise NoSuchElementException('Select all option not found.')

        else:
            NoSuchElementException('Table not found.')


class Text(Element):
    """
        Text object
        ~~~~~~~~~~~~~~~~

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

    def __str__(self):
        return self._text()

    def __unicode__(self):
        return self._text()


# -------------------------------------------------- Complex Structures -----------------------------------------------#
class DropdownForm(Dropdown):
    """
        Dropdown Form object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """Dropdown form element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Dropdown.__init__(self, driver, path)

        self.form = Form(driver, '{0}/following-sibling::*[self::div or self::ul or self::ol]'
                                 '//form[@data-qa-id]'.format(path))

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


class DropdownMenu(Dropdown):
    """
        Dropdown Menu object
        ~~~~~~~~~~~~~~~~

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

        if self.dropdown_list.exists():

            self.expand()

            # Find all items that we can select (click)
            items = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                       '"{1}")]'.format(self.dropdown_list.search_term[1], value))

            if len(items) > 0:
                items[0].click()

            else:
                error = 'Dropdown item {0} cannot be found.'.format(str(value))
                raise NoSuchElementException(error)


class SearchBox(Search):
    """
        Search Box object
        ~~~~~~~~~~~~~~~~

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

    def __init__(self, driver, path):
        """

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Search.__init__(self, driver, path)

        self.results = List(driver, '{0}/following-sibling::*[self::ul or self::ol or self::div]'.format(path))

    def expand(self):
        """Expand result box

        :return:
        """

        if self.exists():
            if self.results.angular_hidden():
                self._click()

    def collapse(self):
        """Close result box

        :return:
        """

        if self.exists():
            if not self.results.angular_hidden():
                self.blur()


class TabNavigation(Element):
    """
        Tab-Navigation object
        ~~~~~~~~~~~~~~~~

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
            items = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                       '"{1}")]'.format(self.search_term[1], value))

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

            selector = '//*[(self::a or self::input or self::button) and @data-qa-id] and contains(@class, "active")'

            # Find all items that we can select (click)
            items = self.driver.find_elements_by_xpath('{0}{1}'.format(self.search_term[1], selector))

            for item in items:
                if item.is_selected():
                    output.append(item)

        return output
