
Page - Web page class
=====================

Pages are considered the scaffolding for interacting with web pages as a whole. While the class is not necessary in
creating testing frameworks, it does contain a few useful functions such as validating that the browser is in view of
that page. An example would look like:

.. code-block:: python

    from sda.page import Page
    from sda.structures import *
    from selenium import webdriver

    class HelloWorld(Page):

        def __init__(self, driver):

            Page.__init__(self, driver, '\/category\/sub-category\/page')  # Make sure that this is a regular expression

            self.foo = Button(driver, '//button[@id="buttonFoo"]')

    wd = webdriver.Firefox()
    h = HelloWorld(wd)

    # Click 'Foo' button
    h.foo.click()

.. automodule:: sda.page
    :members:
    :undoc-members:
    :show-inheritance:
