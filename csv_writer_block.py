from nio.block.base import Block
from nio.properties import *
import csv


class CSVWriter(Block):

    """Create and write to Comma Separated Value files."""

    file = FileProperty(title='File', default='output.csv')
    row = Property(title='Row', default='')
    overwrite = BoolProperty(title='Overwrite File?', default=False)
    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        if self.overwrite():
            file_name = self.file().value
            # csv module requires file objects be opened with newline=''
            with open(file_name, 'w', newline='') as csvfile:
                self.logger.debug('{} opened'.format(file_name))
                for signal in signals:
                    self._write_file(csvfile, signal)
        else:
            for signal in signals:
                file_name = self.file(signal).value
                with open(file_name, 'a', newline='') as csvfile:
                    self.logger.debug('{} opened'.format(file_name))
                    self._write_file(csvfile, signal)

    def _write_file(self, csvfile, signal):
        data = self.row(signal)
        if not isinstance(data, list):
            self.logger.error('row must evaluate to a list')
            return
        csv.writer(csvfile).writerow(data)
        self.logger.debug('{} written to file'.format(data))
