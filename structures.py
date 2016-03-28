from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select as SeleniumSelect
import re

from element import *

__all__ = ['Button', 'Dropdown', 'DropdownForm', 'Form', 'Image', 'List', 'SearchBox', 'Search', 'Select',
           'TabNavigation', 'Table', 'Text']


# ---------------------------------------------------- Base Structures ------------------------------------------------#
class Field(Element):

    def __init__(self, driver, path):
        """Field Element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

    def __str__(self):
        return self.__getitem__('value')

    def __unicode__(self):
        return self.__getitem__('value')

    def is_disabled(self):
        """Returns True, if the button is disabled

        :return:
        :rtype: bool
        """

        return self.__contains__('disabled')


# --------------------------------------------------- Simple Structures -----------------------------------------------#
class Button(Field):

    def __str__(self):
        return self._text()

    def __unicode__(self):
        return self._text()

    def click(self):
        """Click button

        :return:
        """

        return self._click()

    def type(self):
        """Returns button, reset or submit

        :return:
        :rtype: str
        """

        return self.__getitem__('type')


class Div(Element):

    def __init__(self, driver, path):
        """Container element. Includes body, header, footer, section

        :param driver: Selenium webdriver
        :param path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)


class Dropdown(Element):

    def __init__(self, driver, path, dropdown_path=None):
        """Dropdown element

        :param driver: Selenium webdriver
        :param path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

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

    def __init__(self, driver, path):
        """

        :param driver: Selenium webdriver
        :param path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

        self._submit = Button(driver, '{0}//*[contains(@data-qa-id, "submit")]'.format(path))
        self._cancel = Button(driver, '{0}//*[contains(@data-qa-id, "cancel")]'.format(path))

    def __getitem__(self, instance):
        """Get (value) for field instance

        :param instance: id selector
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

        :param instance: id selector
        :param value: Value to set
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

        :param instance: id selector
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

    def __init__(self, driver, path):
        """Embedded image element

        :param driver: Selenium webdriver
        :param path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

    def source(self):
        """Returns link to image file

        :return:
        :rtype: str
        """

        return self.__getitem__('src')


class InputCheckbox(Element):

    def __init__(self, driver, path):
        """Checkable element

        :return:
        """
        Element.__init__(self, driver, By.XPATH, path)

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

        element_id = self.__getitem__('id')

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
    pass


class InputText(Field):

    def input(self, text, clear=True):
        """Assign 'text' as input's value

        :param str text: Text value
        :param bool clear: True, to clear element of previous value
        :return:
        """

        self._input(text, clear)


class Link(Button):

    def href(self):
        self.__getitem__('href')


class List(Element):

    def __init__(self, driver, path):
        """List element. Includes ol and ul

        :param driver: Selenium webdriver
        :param path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

    def items(self):

        if self.exists():

            list_results = {}
            results = self.driver.find_elements_by_xpath('{0}//*[@data-qa-id]'.format(self.search_term[1]))

            for result in results:
                r = re.findall(r'-(\w+)\[(\d+)\]', result.get_attribute('data-qa-id').encode('ascii', 'ignore'))

                if len(r) > 0:

                    result_num = r[0][1]
                    result_type = r[0][0]

                    if result_num in list_results:
                        list_results[result_num][result_type] = result

                    else:
                        list_results[result_num] = {result_type: result}

            return list_results

        return {}

    def item(self, index):

        if self.exists():

            list_results = {}

            if isinstance(index, int):
                results = self.driver.find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                             '"item[{1}]")]'.format(self.search_term[1], str(index)))

            elif isinstance(index, str):

                if index.isdigit():
                    results = self.element().find_elements_by_xpath('{0}//*[contains(@data-qa-id, '
                                                                    '"item[{1}]")]'.format(self.search_term[1], index))
                else:
                    return list_results

            else:
                return list_results

            for result in results:
                r = re.findall(r'-(\w+)\[(\d+)\]', result.get_attribute('data-qa-id').encode('ascii', 'ignore'))

                if len(r) > 0:

                    result_type = r[0][0]

                    if result_type in list_results:
                        list_results[result_type] = result

                    else:
                        list_results[result_type] = result

            return list_results


class Modal(Form):

    def __init__(self, driver, path):

        Form.__init__(self, driver, path)
        self._close = Button(driver, '{0}//*[contains(@data-qa-id, "close")]'.format(path))

    def close(self):
        """Close modal

        :return:
        """

        self._close.click()


class Search(Element):

    def __init__(self, driver, path):
        """Search input element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)
        self._clear = Button(driver, '{0}/following-sibling::span'.format(path))

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


class Select(Element):

    def __init__(self, driver, path):
        """Select element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

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

        :param option: Visible Text, index or value
        :return:
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

        :param option: Visible Text, index or value
        :return:
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

        :return:
        """

        return self._deselect_all()

    def is_disabled(self):
        return self.__contains__('disabled')


class Table(Element):

    ORDERS = ('asc', 'desc', 'none')

    def __init__(self, driver, path):
        Element.__init__(self, driver, By.XPATH, path)

        self._rows = List(driver, '{0}//tbody'.format(path))

    def __getitem__(self, instance):

        rows = self.rows()

        if isinstance(instance, int):
            if str(instance) in rows:
                return rows[str(instance)]

        elif isinstance(instance, str):
            if instance.isdigit():
                if instance in rows:
                    return rows[instance]

        return {}

    @property
    def headers(self):
        """Return a list of table headers

        :return:
        :rtype: list
        """

        element = self.element()

        if element:
            return element.find_elements_by_xpath('.//th[@data-qa-id]')

        return []

    # Determine this out
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

    def filters(self, ):
        """Return a list of all available filters

        :return: Filters
        :rtype: list
        """

        return self.driver.find_elements_by_xpath('//*[contains(@data-qa-id, "asc") or '
                                                  'contains(@data-qa-id, "desc")]/ancestor::th')

    def rows(self):
        """Return a dict of all table data

        :return:
        :rtype: dict
        """

        if self._rows.exists():
            return self._rows.items()

        return {}

    def select_all(self):
        """Click select all checkbox in header

        :return:
        """

        element = self.element()

        if element:
            select_all = element.find_elements_by_xpath('.//th[contains(@data-qa-id, "select-all")]')

            if len(select_all) > 0:
                select_all[0].click()

            else:
                raise NoSuchElementException('Select all option not found.')

        else:
            NoSuchElementException('Table not found.')


class Text(Element):

    def __init__(self, driver, path):
        """Text container. Includes p, span, h1-6 and label

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

    def __str__(self):
        return self._text()

    def __unicode__(self):
        return self._text()


# -------------------------------------------------- Complex Structures -----------------------------------------------#
class DropdownForm(Dropdown):

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

        :return:
        """

        self.form.fields()

    def field(self, instance):
        """

        :param instance:
        :return:
        """

        self.form.field(instance)


class DropdownMenu(Dropdown):

    def select(self, value):
        """Click item within dropdown box

        :param value: id selector
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

    def __init__(self, driver, path):
        """Search field with dropdown results

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
                self._click()


class TabNavigation(Element):

    def __init__(self, driver, path):
        """Tan navigation element

        :param driver: Selenium webdriver
        :param str path: Selector path
        :return:
        """

        Element.__init__(self, driver, By.XPATH, path)

    def select(self, value):
        """Click item within navigation

        :param value: id selector
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

        :return:
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
