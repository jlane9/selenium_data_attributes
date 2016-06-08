
Mixins - Element functionality extensions
=========================================

Mixins allow for elements to "share" common functions with other elements. Elements inherit from the Element base class
and can be "extended" by any number of mixins. An example would be:

.. code-block:: python

    from sda.element import Element
    from sda.mixins import ElementMixin

    class FooMixin(ElementMixin):

        def foo(self):
            return 1

    class BarMixin(ElementMixin):

        def bar(self):
            return 0

    class Foo(Element, FooMixin, BarMixin):

        pass

    f = Foo()

    f.bar()

    # Returns
    0

    f.foo()

    # Returns
    1


.. automodule:: sda.mixins
    :members:
    :undoc-members:
    :show-inheritance:
    :noindex:
    
