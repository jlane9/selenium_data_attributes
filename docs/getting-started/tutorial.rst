Tutorial
--------

After installing sda you should be ready to begin.


Starting a project
^^^^^^^^^^^^^^^^^^

SDA is built on principle that it will be used in conjunction with development. A developer would develop their web site
using uniquely identifiable ids or attributes to locate elements within a web page. SDA allows the test builders to
create a "framework" that all tests can generally be written on top of so that the tests are not brittle
(simple changes easily break operability and fixing requires extensive re-work). When beginning a project it is best
practice to already start thinking of how the framework structure will come together. An example would be:

my_site
    - hello_page
        - page.py
    - goodbye_page
        - page.py
    - website
        - site.py
