from nio.block.base import Block
from nio.properties import Property
import csv


class CSVWriter(Block):

    file = Property(title='File', default='output.csv')
    row = Property(title='Row', default='')

    def process_signals(self, signals):
        for signal in signals:
            file_name = self.file(signal)
            data = self.row(signal)
            if type(data) != type(list()):
                self.logger.exception(
                    'row must evaluate to a list'
                )
            else:
                with open(file_name, 'a', newline='') as csvfile:
                    self.logger.debug(
                        '{} opened'.format(file_name)
                    )
                    csv.writer(csvfile).writerow(data)
                    self.logger.debug(
                        '{} appended to end of file'.format(data)
                    )
