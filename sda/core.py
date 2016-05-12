"""Core

.. automodule:: sda.core
    :platform: Unix, Windows
    :synopsis: This module stores common functionality throughout sda
    :copyright: (c) 2016 FanThreeSixty
    :moduleauthor: John Lane <jlane@fanthreesixty.com>
    :license: MIT, see LICENSE for more details.
"""

__author__ = 'jlane'
__copyright__ = 'Copyright (c) 2016 FanThreeSixty'
__license__ = "MIT"
__version__ = '0.4.6'
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
def encode_ascii(func):
    """

    :param func: Function returns text as ascii
    :return:
    """

    def func_wrapper(self):

        text = func(self)

        # Convert UNICODE to ASCII
        if isinstance(text, unicode) or isinstance(text, str):
            return text.encode('ascii', 'ignore')

        # Iterate list of UNICODE strings to ASCII
        elif isinstance(text, list) or isinstance(text, tuple):
            return [item.encode('ascii', 'ignore') for item in text
                    if isinstance(item, unicode) or isinstance(item, str)]

        return ''

    return func_wrapper
