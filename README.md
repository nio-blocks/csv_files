CSVReader
=========
Read lines from a CSV file. For each incoming signal, one row is read from `file`.

Properties
----------
- **file**: File path to open and read.
- **loop**: Return to start of file when out of lines.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals of equal length to input signals.
  - *row* (array) The next line of the file, where each value (cell) of the row is an element of the array.

Commands
--------
None

***

CSVWriter
=========
Write to a CSV file. For each incoming signal `row` is appended to `file`.

Properties
----------
- **file**: File name to write CSV data to.
- **row**: Data to write to the CSV file.

Inputs
------
- **default**: Any list of signals with data to write.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
None

