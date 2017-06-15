CSVWriter
=========
Create and write to Comma Separated Value files.

Properties:
-----------
`file` (str): File path/name to write to, will be created if not found. 
Should end with `.csv` file extension.
`row` (list): Each element of `row` is written to the last line of `file`, 
in order, seperated by commas. Will log an error if `row` does not evaluate as 
a list.
`overwrite` (bool): If True, each list of signals processed will open `file`, 
overwriting if it exists, and each signal will write one row. If False, each 
signal in a list opens and appends `row` to the end of `file`.

Dependencies:
-------------
None

Commands:
---------
None

Input:
------
Any list of signals where each signal evaluates as a list.

Output:
-------
None
