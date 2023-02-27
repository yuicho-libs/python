#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import logging

# Additional library

# Original library

# Other module


#----------------------------------------------------------
# Init
#----------------------------------------------------------
# Get logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# Previous memory
_previous_dict = dict()


#----------------------------------------------------------
# Functions
#----------------------------------------------------------
def is_first_seen(key, value):
    if key not in _previous_dict:
        _previous_dict[key] = list()

    _logger.debug('value = %s' % value)
    _logger.debug('_previous_dict[%s] = %s' % (key,_previous_dict[key]))
    if value in _previous_dict[key]:
        return False

    _previous_dict[key].append(value)
    return True


def is_key_exists(key):
    result = key in _previous_dict

    _logger.debug(f'Check exists [{key}] ---> {result}')
    return result


#----------------------------------------------------------
# for DEBUG
#----------------------------------------------------------
if __name__ == '__main__':
    pass
