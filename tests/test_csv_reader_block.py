from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import patch, MagicMock, mock_open

from ..csv_reader_block import CSVReader


class TestReadLines(NIOBlockTestCase):

    def test_process_signals(self):
        """read and notify one row per incoming signal, return to 
        start of file when out of rows"""
        blk = CSVReader()
        rows = [['foo', 0], ['bar', 1], ['baz', 2]]
        # an exception is raised and handled at end of file
        lines = rows + [StopIteration] + rows
        m = mock_open()
        with patch(blk.__module__ + '.csv') as mock_csv:
            with patch('builtins.open', m):
                mock_reader = mock_csv.reader.return_value
                mock_reader.__next__.side_effect = lines
                self.configure_block(blk, {'file': 'foo.csv'})
                blk.start()
                blk.process_signals([Signal()] * 6)
                # out of lines, loop back to beginning and continue
                self.assertEqual(m.return_value.seek.call_count, 1)
                self.assert_num_signals_notified(6)
                # three lines have been read and notified twice
                self.assert_signal_list_notified(
                    [Signal({'row': line}) for line in rows * 2])
        blk.stop()

    def test_out_of_rows(self):
        """when out of rows and loop=False, log a warning and notify 
        available rows"""
        blk = CSVReader()
        lines = [['foo', 0], ['bar', 1]]
        m = mock_open()
        with patch(blk.__module__ + '.csv') as mock_csv:
            with patch('builtins.open', m):
                mock_reader = mock_csv.reader.return_value
                mock_reader.__next__.side_effect = lines
                self.configure_block(blk, {'file': 'foo.csv', 'loop': False})
                blk.start()
                # three signals, only two rows available, log warning
                blk.process_signals([Signal()] * 3)
                self.assert_num_signals_notified(2)
                self.assert_signal_list_notified(
                    [Signal({'row': line}) for line in lines])
        blk.stop()
