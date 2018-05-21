from os import getenv


TIMEOUT = int(getenv('TIMEOUT', '60'))
MIN_ENTITY_LENGTH = int(getenv('MIN_ENTITY_LENGTH', '2'))
MATCH_RATIO = int(getenv('MATCH_RATIO', '75'))
