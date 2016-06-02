"""Core
"""

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.6.0'
__contact__ = 'jlane@fanthreesixty.com'
__status__ = 'Alpha'
__docformat__ = 'reStructuredText'

__all__ = ['ASC_IDENTIFIER', 'CANCEL_IDENTIFIER', 'CLEAR_IDENTIFIER', 'CLOSE_IDENTIFIER', 'DEFAULT_IDENTIFIER',
           'DESC_IDENTIFIER', 'SELECT_ALL_IDENTIFIER', 'SUBMIT_IDENTIFIER', 'encode_ascii']

# GLOBAL VARIABLES
DEFAULT_IDENTIFIER = 'data-qa-id'

ASC_IDENTIFIER = 'asc'
CANCEL_IDENTIFIER = 'cancel'
CLEAR_IDENTIFIER = 'clear'
CLOSE_IDENTIFIER = 'close'
DESC_IDENTIFIER = 'desc'
SELECT_ALL_IDENTIFIER = 'select-all'
SUBMIT_IDENTIFIER = 'submit'


# Shortcuts
def encode_ascii(clean=False):
    """Function returns text as ascii

    :param clean: True, to delete trailing spaces
    :return:
    """
    def encode_ascii_decorator(func):

        def func_wrapper(*args, **kwargs):

            text = func(*args, **kwargs)

            # Convert UNICODE to ASCII
            if isinstance(text, unicode) or isinstance(text, str):

                if clean:
                    return text.encode('ascii', 'ignore').strip()

                return text.encode('ascii', 'ignore')

            # Iterate list of UNICODE strings to ASCII
            elif isinstance(text, list) or isinstance(text, tuple):

                if clean:
                    return [item.encode('ascii', 'ignore').strip() for item in text
                            if isinstance(item, unicode) or isinstance(item, str)]

                return [item.encode('ascii', 'ignore') for item in text
                        if isinstance(item, unicode) or isinstance(item, str)]

            return ''

        return func_wrapper

    return encode_ascii_decorator
