from nio.block.base import Block
<<<<<<< HEAD
from nio.properties import Property, VersionProperty
=======
from nio.properties import Property
>>>>>>> 15c45c44f113dca6ac45bb14f8d1bab5b44fba3f
import csv


class CSVWriter(Block):

    file = Property(title='File', default='output.csv') # file property
    row = Property(title='Row', default='')
    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        for signal in signals:
            file_name = self.file(signal)
            data = self.row(signal)
            if not isinstance(data, list):
                self.logger.error('row must evaluate to a list')
                continue
            # csv module requires file objects be opened with newline=''
            with open(file_name, 'a', newline='') as csvfile:
                self.logger.debug(
                    '{} opened'.format(file_name)
                )
<<<<<<< HEAD
                csv.writer(csvfile).writerow(data)
                self.logger.debug(
                    '{} appended to end of file'.format(data)
                )
=======
            else:
                with open(file_name, 'a', newline='') as csvfile:
                    self.logger.debug(
                        '{} opened'.format(file_name)
                    )
                    csv.writer(csvfile).writerow(data)
                    self.logger.debug(
                        '{} appended to end of file'.format(data)
                    )
>>>>>>> 15c45c44f113dca6ac45bb14f8d1bab5b44fba3f
