# Custom Archivator

## Purpose

Compressing files.

## Input Data

Any file.

## Output Data

File in 32a format.

## Structure Of 32a File

- 3 bytes to define the file format.
- 2 bytes to define the length dictionary.
- dictionary.
- output stream.

## Algorithm

### Archiving

1. Getting input file and spliting into blocks of weight 3 bytes.
2. Creating dictionary.
3. If the block is in the dictionary, then the value of the block is added to the dictionary.
4. If the block is not in the dictionary, then 2 bytes are written to the output stream, corresponding to then block in dictionary.
5. Collecting in a single file, the structure of which is described above.

note: if the block size is not a multiple of 3 or the dictionary is full, then the control bytes “FFFFh” are set, and then the current 3 bytes (or the remaining 1 or 2 bytes at the end of the file) are written to the output stream unchanged.

### Dearchiving

1. Getting the input file, reading the first 3 bytes to determine the file format, i.e. check the archive identifier.
2. If the identifier is appropriate, reading the next 2 bytes - the length of the dictionary.
3. Reading the dictionary of the corresponding number of bytes.
4. Formation the output stream. Spliting the data by 2 bytes and compare the blocks with the dictionary, writting them to the receiving output stream.

note: when a 2-byte indicator "FFFFh" is detected during unarchiving, the 3 bytes following the indicator are written without conversion to the receiving output stream. If, after the indicator, there are less than 3 bytes to the end of the file, then these bytes are written unchanged into the receiving output stream.

## Getting Started

### Prerequisites

To run the project, you need to have Python 3.7+.

### Installation

1. Clone the repo
```bash
$ git clone https://github.com/Alexey-Chegodaykin/source-coding.git
```

### Usage

1. Run Python script
```bash
$ python main.py -file FILE -type TYPE -fmt FMT
```
- FILE - path to target file.
- TYPE - type of running (0 - archivate, 1 - dearchivate).
- FMT - dearchivate file format (default .txt).
