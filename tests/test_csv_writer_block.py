from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import patch, MagicMock, mock_open
from ..csv_writer_block import CSVWriter


class TestWriteLines(NIOBlockTestCase):

    input_signals = [Signal({'file': 'name0', 'key': 'value0'}),
                     Signal({'file': 'name1', 'key': 'value1'})]

    def test_process_signals(self):
        blk = CSVWriter()
        self.configure_block(blk, {'file': '{{ $file }}',
                                   'row': '{{ [$key] }}'})
        blk.start()
        m = mock_open()
        with patch('builtins.open', m):
            blk.process_signals(self.input_signals)
            for i, call in enumerate(m.call_args_list):
                self.assertEqual(
                    call[0][0],
                    self.input_signals[i].to_dict()['file'])
            for i, call in enumerate(m().write.call_args_list):
                self.assertEqual(
                    call[0][0],
                    self.input_signals[i].to_dict()['key'] + '\r\n')
        blk.stop()

    def test_bad_data(self):
        """row does not evaluate to a list, error logged"""
        blk = CSVWriter()
        self.configure_block(blk, {'file': '{{ $file }}',
                                   'row': '{{ $key }}'})
        blk.logger = MagicMock()
        blk.start()
        m = mock_open()
        with patch('builtins.open', m):
            blk.process_signals(self.input_signals)
        self.assertEqual(blk.logger.error.call_count, 2)
        blk.stop()

    def test_overwrite(self):
        blk = CSVWriter()
        self.configure_block(blk, {'file': 'file',
                                   'row': '{{ [$key] }}',
                                   'overwrite': True})
        input_signals = [Signal({'key': 'value0'}), Signal({'key': 'value1'})]
        blk.start()
        m = mock_open()
        with patch('builtins.open', m):
            blk.process_signals(self.input_signals)
            m.assert_called_once_with('file', 'w', newline='')
            for i, call in enumerate(m().write.call_args_list):
                self.assertEqual(
                    call[0][0],
                    self.input_signals[i].to_dict()['key'] + '\r\n')
        blk.stop()
