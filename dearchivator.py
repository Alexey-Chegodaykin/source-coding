from itertools import product
from typing import List
from settings import FORMAT, COUNT_FORMAT_BYTES, COUNT_DICTIONARY_SIZE_BYTES
from settings import ENCODING_BATCH_SIZE, REPLACEMENT_BATCH_SIZE, MAX_BYTE_VALUE, CONTROL_BYTES


class Dearchivator:
    def _compute_output_stream(self, path_input_file: str) -> List[bytes]:
        file_name: str = path_input_file.split('\\')[-1]
        dictionary: dict = {}
        output_stream: List[bytes] = []
        values_combinations: iter = product(range(MAX_BYTE_VALUE + 1), repeat=REPLACEMENT_BATCH_SIZE)

        with open(file_name, 'rb') as fin:
            data: bytes = fin.read()
            format: List = [data[ind] for ind in range(COUNT_FORMAT_BYTES)]
        
            if bytes(format) != bytes(FORMAT.encode()):
                fin.close()
                raise Exception('Current archive format does not support.')
            else:
                dictionary_len: int = (data[3] * (MAX_BYTE_VALUE + 1) + data[4]) * ENCODING_BATCH_SIZE
                start_dictionary_position: int = COUNT_FORMAT_BYTES + COUNT_DICTIONARY_SIZE_BYTES
                keys_ind: List[int] = range(start_dictionary_position, dictionary_len + start_dictionary_position, ENCODING_BATCH_SIZE)

                for ind, item in zip(keys_ind, values_combinations):
                    key: bytes = bytes([value for value in item])
                    value: bytes = data[ind:ind+ENCODING_BATCH_SIZE]
                    dictionary[key] = value

                iteraion: int = COUNT_FORMAT_BYTES + COUNT_DICTIONARY_SIZE_BYTES + dictionary_len
                data_len = len(data)
                
                output_stream.append(list(dictionary.values())[0])
        
                while iteraion < data_len:
                    byte: bytes = data[iteraion:iteraion+REPLACEMENT_BATCH_SIZE]
                
                    if byte == CONTROL_BYTES:
                        if data_len - (iteraion + REPLACEMENT_BATCH_SIZE) < ENCODING_BATCH_SIZE:
                            byte = data[iteraion+REPLACEMENT_BATCH_SIZE:iteraion+REPLACEMENT_BATCH_SIZE+REPLACEMENT_BATCH_SIZE]
                            output_stream.append(byte)
                            iteraion += REPLACEMENT_BATCH_SIZE
                        else:
                            byte = data[iteraion+REPLACEMENT_BATCH_SIZE:iteraion+REPLACEMENT_BATCH_SIZE+ENCODING_BATCH_SIZE]
                            output_stream.append(byte)
                            iteraion = iteraion + REPLACEMENT_BATCH_SIZE + ENCODING_BATCH_SIZE
                    else:
                        dictionary_value = dictionary[byte]
                        output_stream.append(dictionary_value)
                            
                    iteraion += REPLACEMENT_BATCH_SIZE
                
                fin.close()

            return output_stream

    def _output_file_writting(self, path_input_file: str, target_format: str, output_stream: List[bytes]) -> None:
        file_name = path_input_file.split('\\')[-1]

        with open(file_name.split('.')[0] + target_format, 'wb') as fout:
            for bytes_ in output_stream:
                fout.write(bytes_)
            fout.close()

    def dearchivate(self, path_input_file: str, target_format: str):
        output_stream: List[bytes] = self._compute_output_stream(path_input_file)
        self._output_file_writting(path_input_file, target_format, output_stream)
        print('Dearchivate is completed successfully.')
