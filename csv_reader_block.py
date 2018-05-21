import csv

from nio import Signal, Block
from nio.properties import BoolProperty, FileProperty, VersionProperty


class CSVReader(Block):

    file = FileProperty(title='File', default='input.csv')
    loop = BoolProperty(title='Loop?', default=True)
    version = VersionProperty("0.1.1")

    def __init__(self):
        super().__init__()
        self.reader = None
        self.csvfile = None

    def start(self):
        super().start()
        # csv module requires file objects be opened with newline=''
        self.csvfile = open(self.file().value, newline='')
        self.logger.debug('{} opened'.format(self.csvfile))
        self.reader = csv.reader(self.csvfile)

    def stop(self):
        super().stop()
        self.csvfile.close()

    def process_signals(self, signals):
        output = []
        for signal in signals:
            fail = False
            try:
                row = self.reader.__next__()
                output.append(Signal({'row': row}))
            except StopIteration as e:
                if self.loop():
                    self.csvfile.seek(0)
                    row = self.reader.__next__()
                    output.append(Signal({'row': row}))
                else:
                    pass
                    fail = True
        self.logger.debug('notifying {} signals'.format(len(output)))
        self.notify_signals(output)
        if fail:
            self.logger.warning('out of rows, {} signals dropped'.format(len(signals) - len(output)))
