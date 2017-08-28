from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from unittest.mock import patch, MagicMock, mock_open

from ..csv_writer_block import CSVWriter


class TestWriteLines(NIOBlockTestCase):

    def test_process_signals(self):
        blk = CSVWriter()
        self.configure_block(blk, {
            'file': '{{ $file }}',
            'row': '{{ [$key] }}',
        })
        blk.start()
        m = mock_open()
        with patch('builtins.open', m):
            blk.process_signals([Signal({
                'file': 'name',
                'key': 'value',
            })])
            m.assert_called_once_with('name', 'a', newline='')
            m().write.assert_called_once_with('value\r\n')
        blk.stop()

    def test_bad_data(self):
        """row does not evaluate to a list, error logged"""
        blk = CSVWriter()
        self.configure_block(blk, {
            'file': '{{ $file }}',
            'row': '{{ $key }}',
        })
        blk.logger = MagicMock()
        blk.start()
        m = mock_open()
        with patch('builtins.open', m):
            blk.process_signals([Signal({
                'file': 'name',
                'key': 'value',
            })])
        blk.logger.error.assert_called_once_with(
            'row must evaluate to a list'
        )
        blk.stop()
