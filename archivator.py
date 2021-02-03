from itertools import product
from typing import List
from settings import FORMAT, ENCODING_BATCH_SIZE, REPLACEMENT_BATCH_SIZE
from settings import MAX_BYTE_VALUE, MAX_DICTIONARY_SIZE, CONTROL_BYTES


class Archivator:
    @staticmethod
    def _is_dictionary_overflow(dictionary: dict, max_size: int) -> bool:
        return False if len(dictionary) < max_size else True

    @staticmethod
    def _dictionary_byte_size(dictionary: dict, max_byte: int) -> bytes:
        if dictionary:
            count_keys = len(dictionary)
            return bytes([count_keys // (max_byte + 1), count_keys % (max_byte + 1)])
        else:
            raise Exception('Dictionary is empty.')

    @staticmethod
    def _compressing(input_bytes: int, output_bytes: int) -> float:
        return round(((input_bytes - output_bytes) / input_bytes) * 100, 2)

    def _input_file_splitting(self, path_input_file: str) -> List[bytes]:
        batches: List[bytes] = []
        
        with open(path_input_file, 'rb') as fin:
            data: bytes = fin.read()
            
            if data:
                for ind in range(0, len(data), ENCODING_BATCH_SIZE):
                    batch: bytes = data[ind:ind+ENCODING_BATCH_SIZE]
                    batches.append(batch)
                fin.close()
            else:
                fin.close()
                raise Exception('Archived file is empty.')

        return batches

    def _compute_output_stream(self, batches: List[bytes]) -> tuple:
        output_stream: List[bytes] = []
        dictionary: dict = {}
        values_combinations: iter = product(range(MAX_BYTE_VALUE + 1), repeat=REPLACEMENT_BATCH_SIZE)
        
        if batches:
            for ind, batch in enumerate(batches):
                if (len(batch) % ENCODING_BATCH_SIZE) != 0:
                    output_stream.append(CONTROL_BYTES)
                    output_stream.append(batch)
                    break

                if batch not in dictionary.keys():
                    if not self._is_dictionary_overflow(dictionary, MAX_DICTIONARY_SIZE):
                        dict_value = bytes([value for value in next(values_combinations)])
                        dictionary[batch] = dict_value
                        if ind != 0: output_stream.append(dict_value)
                    else:
                        output_stream.append(CONTROL_BYTES)
                        output_stream.append(batch)
                else:
                    dictionary_value = dictionary[batch]
                    output_stream.append(dictionary_value)
            
        else:
            raise Exception('Batches not found.')

        return dictionary, output_stream

    def _output_file_writting(self, path_input_file: str, format: bytes, 
                              dictionary_byte_size: bytes, dictionary: dict, 
                              output_stream: List[bytes]) -> None:

        file_name: str = path_input_file.split('\\')[-1]

        with open(file_name.split('.')[0] + '.' + FORMAT, 'wb') as fout:
            fout.write(format)
            fout.write(dictionary_byte_size)
            
            for key in dictionary.keys():
                fout.write(key)

            for bytes_ in output_stream:
                fout.write(bytes_)
            fout.close()

    def archivate(self, path_input_file: str) -> None:
        format: bytes = bytes(FORMAT.encode())
        input_batches: List[bytes] = self._input_file_splitting(path_input_file)
        dictionary, output_stream = self._compute_output_stream(input_batches)
        dictionary_byte_size: bytes = self._dictionary_byte_size(dictionary, MAX_BYTE_VALUE)
        input_bytes: int = len(input_batches) * ENCODING_BATCH_SIZE
        output_bytes: int = len(output_stream) * REPLACEMENT_BATCH_SIZE + \
                            len(dictionary) * ENCODING_BATCH_SIZE + ENCODING_BATCH_SIZE + REPLACEMENT_BATCH_SIZE

        compressing: float = self._compressing(input_bytes, output_bytes)

        self._output_file_writting(path_input_file, format, dictionary_byte_size, dictionary, output_stream)

        print('Archivate is completed successfully.')
        print(f'Compression ratio is {compressing} %')
