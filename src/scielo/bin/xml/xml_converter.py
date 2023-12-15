import logging
import sys

from app_modules.app import xc
from app_modules.generics import encoding


def requirements_checker():
    try:
        import PIL
    except Exception as e:
        print("pillow is not installed as expected: %s %s" % (type(e), e))
        logging.exception(e)
    try:
        import packtools
    except Exception as e:
        print("packtools is not installed as expected: %s %s" % (type(e), e))
        logging.exception(e)


if __name__ == '__main__':
    parameters = encoding.fix_args(sys.argv)
    requirements_checker()
    xc.call_converter(parameters, '1.1')
