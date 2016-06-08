
Core functions
==============

Core functions are reusable shortcuts that all elements can use.

.. autofunction:: sda.core.encode_ascii

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


