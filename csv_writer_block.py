import csv

from nio import TerminatorBlock
from nio.properties import Property, FileProperty, VersionProperty


class CSVWriter(TerminatorBlock):

    file = FileProperty(title='File', default='output.csv')
    row = Property(title='Row', default='')
    version = VersionProperty("0.1.0")

    def process_signals(self, signals):
        for signal in signals:
            file_name = self.file(signal).value
            data = self.row(signal)
            if not isinstance(data, list):
                self.logger.error('row must evaluate to a list')
                continue
            # csv module requires file objects be opened with newline=''
            with open(file_name, 'a', newline='') as csvfile:
                self.logger.debug('{} opened'.format(file_name))
                csv.writer(csvfile).writerow(data)
                self.logger.debug('{} appended to end of file'.format(data))
