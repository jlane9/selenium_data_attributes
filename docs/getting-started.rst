2. Getting Started
------------------

2.1 Sample project
^^^^^^^^^^^^^^^^^^

After installing sda you should be ready to begin.

SDA is built with the intention that it will be used in conjunction with web development. A developer would develop
their web site using uniquely identifiable ids or attributes to locate elements within a web page. SDA allows the
test builders to create a "framework" that all tests can generally be written on top of so that the tests are not brittle
(simple changes easily break operability and fixing requires extensive re-work. When beginning a testing project, it is
best practice to already start thinking of how that framework structure will come together. An example would be:

my_site
   - hello_page
      - __init__.py
      - fixtures.py
      - locators.py
      - page.py
   - goodbye_page
      - __init__.py
      - fixtures.py
      - locators.py
      - page.py
   - website
      - __init__.py
      - site.py


Each "page" would have its own locators for elements and fixtures which are just elements or collections of elements
with defined structures and have specific behaviours.


2.2 Using SDA to define pages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within each page you need to define each element that may appear on that page. And for each element you need to define
how one might find that element and only that element. For example on hello page there might be a form that the user
would fill out.

.. code-block:: html

   <form id="form_hello">
      <input id="hello_name" placeholder="What is your name?" />
      <input id="hello_submit" type="submit" />
   </form>

To define that form, or "fixture", we would do something similar to the following:

.. code-block:: python

   # First we would start out in the locators.py file
   from sda.locators import Locators
   from selenium.webdrivers.common.by import By

   class HelloLocators(Locators):

      FORM_HELLO = (By.XPATH, '//form[@id="form_hello"]')
      FORM_NAME = (By.XPATH, '//input[@id="hello_name"]')
      FORM_SUBMIT = (By.XPATH, '//input[@id="hello_submit"]')


.. code-block:: python

   # Then we would move to the fixtures.py file
   from sda.element import Element
   from sda.structures import *
   from locators import HelloLocators

   class HelloForm(Element):

      def __init__(self, web_driver, by, path):

         super(HelloForm, self).__init__(web_driver, by, path)

         hello = InputText(web_driver, *HelloLocators.FORM_NAME)
         submit = Button(web_driver, *HelloLocators.FORM_SUBMIT)


.. code-block:: python

   # Lastly we would add that fixture to page.py
   from sda.page import Page
   from fixtures import HelloForm
   from locators import HelloLocators

   class HelloPage(Page):

      def __init__(self, web_driver):

         super(HelloPage, self).__init__(web_driver)

         form = HelloForm(web_driver, *HelloLocators.FORM_HELLO)


.. code-block:: python

   # Once the page is complete, add it to the main site
   from sda.site import Site
   from my_site.hello_page.page import HelloPage

   class MySite(Site):

      def __init__(self, web_driver):

         super(MySite, self).__init__(web_driver)

         hello = HelloPage(web_driver)