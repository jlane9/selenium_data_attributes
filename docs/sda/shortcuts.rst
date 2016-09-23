
Core functions
==============

Core functions are reusable shortcuts that all elements can use.

.. autofunction:: sda.shortcuts.encode_ascii

Since all text returns from selenium as unicode, it's useful to have a means to convert that text to ASCII so
python can more adeptly use what is returned. To use encode_ascii simply add it before a class method.

.. code-block:: python

    from sda.core import encode_ascii

    class Foo(object):

        @encode_ascii()
        def bar(self):

            return u'hello world'


    f = Foo()
    f.bar()

    # Returns
    'hello world'

    type(f.bar())

    # Returns
    'str'

.. autofunction:: sda.shortcuts.generate_elements



.. code-block:: python

    from sda.core import generate_elements
    from sda.element import Element
    from selenium.webdriver.common.by import By
    from selenium import webdriver

    # Locator
    class FooLocators(object):

        BAR_LOCATOR = (By.XPATH, '//some/locator')

    # Can be fixture or structure
    class Bar(object):

        def __init__(self, web_driver, by, path):

            self._driver = web_driver
            self.element = Element(web_driver=web_driver, by=by, path=path)

    # Can be fixture or page
    class Foo(object):

        def __init__(self, web_driver):
            self.driver = web_driver

        # Essentially what generate elements will do is find all elements that return from the selector and then append
        # an index at the end of the selector expression. Make sure to use XPATH. There will be support for other
        # selector types other than By.XPATH, but this is the only way that it will properly work. Always remember to
        # return the web driver element!
        @generate_elements(Bar, FooLocators.BAR_LOCATOR)
        def bars(self):

            return self.driver

    wd = webdriver.Firefox()
    f = Foo(wd)

    # Returns all the foobar instances it can find
    bars = f.bars()

