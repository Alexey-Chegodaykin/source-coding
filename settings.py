FORMAT: str = '32a'
COUNT_FORMAT_BYTES: int = 3
COUNT_DICTIONARY_SIZE_BYTES: int = 2
ENCODING_BATCH_SIZE: int = 3
REPLACEMENT_BATCH_SIZE: int = 2
MAX_BYTE_VALUE: int = 255
MAX_DICTIONARY_SIZE: int = 255 * 256 + 255
CONTROL_BYTES: bytes = bytes([255, 255])