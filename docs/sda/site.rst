
Site - Web site project class
=============================

Similar to Page, Site contains useful functions on the site-level. An example would look like:

.. code-block:: python

    from sda.page import Page
    from sda.site import Site
    from sda.structures import *
    from selenium import webdriver

    class MyPage(Page):

        def __init__(self, driver):

        Page.__init__(self, driver, '/category/sub-category/page')  # Make sure that this is the path only

        self.bar = Button(driver, '//button[@id="buttonBar"]')


    class MySite(Site):

        def __init__(self, driver):

        Site.__init__(self, driver)

        self.foo = MyPage(driver)

    wd = webdriver.Firefox()
    site = MySite(wd)

    # Click 'Bar' button on page 'Foo'
    site.foo.bar.click()

.. automodule:: sda.site
    :members:
    :undoc-members:
    :exclude-members: RE_URL
    :show-inheritance:
    