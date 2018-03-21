from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import patch, MagicMock, mock_open

from ..csv_reader_block import CSVReader


class TestReadLines(NIOBlockTestCase):

    def test_process_signals(self):
        blk = CSVReader()
        lines = ['foo', 'bar', 'baz']
        m = mock_open()
        with patch(blk.__module__ + '.csv') as mock_csv:
            with patch('builtins.open', m):
                mock_reader = mock_csv.reader.return_value
                mock_reader.__next__.side_effect = lines
                self.configure_block(blk, {'file': 'foo.csv'})
                blk.start()
                blk.process_signals([Signal()] * 3)
                m.assert_called_once_with('foo.csv', newline='')
                self.assertEqual(mock_reader.__next__.call_count, 3)
        blk.stop()
        self.assert_num_signals_notified(3)
        self.assert_signal_list_notified(
            [Signal({'line': line}) for line in lines])

    def test_loop(self):
        blk = CSVReader()
        lines = ['foo', 'bar', 'baz', StopIteration]
        m = mock_open()
        with patch(blk.__module__ + '.csv') as mock_csv:
            with patch('builtins.open', m):
                def process_sigs():
                    blk.process_signals([Signal()] * 3)
                mock_reader = mock_csv.reader.return_value
                mock_reader.__next__.side_effect = lines
                self.configure_block(blk, {'loop': True})
                blk.start()
                process_sigs()
                # out of lines, loop back to beginning
                self.assertRaises(StopIteration, process_sigs)
                self.assertEqual(m.return_value.seek.call_count, 1)
        blk.stop()
